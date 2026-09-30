//! Thin JSON batch process boundary for the exact rectangle-density kernel.

use std::io::{self, BufRead, Read, Write};
use std::process::ExitCode;

const MAX_INPUT_BYTES: u64 = 64 * 1024 * 1024;

fn run_one_shot() -> Result<(), String> {
    let mut input = Vec::new();
    io::stdin()
        .lock()
        .take(MAX_INPUT_BYTES + 1)
        .read_to_end(&mut input)
        .map_err(|error| format!("cannot read batch: {error}"))?;
    if input.len() as u64 > MAX_INPUT_BYTES {
        return Err("batch exceeds the input byte limit".into());
    }
    let text =
        std::str::from_utf8(&input).map_err(|error| format!("batch is not UTF-8: {error}"))?;
    let output = sqverify_exact::evaluate(text)?;
    let mut stdout = io::BufWriter::new(io::stdout().lock());
    stdout
        .write_all(output.as_bytes())
        .map_err(|error| format!("cannot write result: {error}"))?;
    stdout
        .write_all(b"\n")
        .map_err(|error| format!("cannot write result: {error}"))?;
    stdout
        .flush()
        .map_err(|error| format!("cannot flush result: {error}"))
}

fn read_line_bounded(reader: &mut impl BufRead) -> Result<Option<Vec<u8>>, String> {
    let mut line = Vec::new();
    loop {
        let available = reader
            .fill_buf()
            .map_err(|error| format!("cannot read session line: {error}"))?;
        if available.is_empty() {
            return if line.is_empty() {
                Ok(None)
            } else {
                Err("session line is missing its newline".into())
            };
        }
        let take = available
            .iter()
            .position(|byte| *byte == b'\n')
            .map_or(available.len(), |index| index + 1);
        if line.len() + take > usize::try_from(MAX_INPUT_BYTES).unwrap_or(usize::MAX) + 1 {
            return Err("session line exceeds the input byte limit".into());
        }
        line.extend_from_slice(&available[..take]);
        reader.consume(take);
        if line.last() == Some(&b'\n') {
            line.pop();
            return Ok(Some(line));
        }
    }
}

fn write_line(writer: &mut impl Write, value: &str) -> Result<(), String> {
    writer
        .write_all(value.as_bytes())
        .and_then(|()| writer.write_all(b"\n"))
        .and_then(|()| writer.flush())
        .map_err(|error| format!("cannot write session response: {error}"))
}

fn run_session() -> Result<(), String> {
    let stdin = io::stdin();
    let mut reader = io::BufReader::new(stdin.lock());
    let stdout = io::stdout();
    let mut writer = io::BufWriter::new(stdout.lock());
    let opening = read_line_bounded(&mut reader)?
        .ok_or_else(|| "session opening table is missing".to_string())?;
    let opening = std::str::from_utf8(&opening)
        .map_err(|error| format!("opening line is not UTF-8: {error}"))?;
    let mut table = sqverify_exact::open_session(opening)?;
    let ready = serde_json::json!({
        "version": 1,
        "status": "ready",
        "table_sha256": table.sha256(),
        "rectangle_count": table.rectangle_count(),
    });
    write_line(&mut writer, &ready.to_string())?;
    while let Some(query) = read_line_bounded(&mut reader)? {
        let query = std::str::from_utf8(&query)
            .map_err(|error| format!("query line is not UTF-8: {error}"))?;
        let answer = sqverify_exact::query_session(&mut table, query)?;
        write_line(&mut writer, &answer)?;
    }
    Ok(())
}

fn run() -> Result<(), String> {
    let mut arguments = std::env::args_os().skip(1);
    match (arguments.next(), arguments.next()) {
        (None, None) => run_one_shot(),
        (Some(mode), None) if mode == "--serve" => run_session(),
        _ => Err("expected no arguments or only --serve".into()),
    }
}

fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("sqverify-exact: {error}");
            ExitCode::FAILURE
        }
    }
}
