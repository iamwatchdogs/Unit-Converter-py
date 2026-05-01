from pytest import CaptureFixture

from unit_converter.main import main


def test_main(capsys: CaptureFixture[str]) -> None:
    """Test the main function's output to be on stdout stream."""
    main()

    output_stream = capsys.readouterr()
    assert output_stream.out != "", "Output should be captured on stdout stream"
    assert output_stream.err == "", "No errors should be captured on stderr stream"

    output_value = output_stream.out
    expected = "Hello from unit-converter!"
    assert output_value.strip() == expected, "Output should match expected message"
