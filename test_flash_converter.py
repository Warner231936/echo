import textwrap

from flash_converter import FlashConverter


def test_basic_conversion(tmp_path):
    src_code = textwrap.dedent(
        """
        var x:int = 1;
        trace('hi');
        function greet(name:String):void {
            trace(name);
        }
        """
    ).strip()

    converter = FlashConverter()
    js = converter.convert_code(src_code)

    expected = textwrap.dedent(
        """
        let x = 1;
        console.log('hi');
        function greet(name) {
            console.log(name);
        }
        """
    ).strip()

    assert js == expected

    # File based API
    src_file = tmp_path / "sample.as"
    dest_file = tmp_path / "sample.js"
    src_file.write_text(src_code)
    converter.convert_file(src_file, dest_file)
    assert dest_file.read_text() == expected


def test_directory_conversion(tmp_path):
    src_root = tmp_path / "src"
    dest_root = tmp_path / "out"
    (src_root / "level1").mkdir(parents=True)

    code = textwrap.dedent(
        """
        var score:int = 0;
        function log(msg:String):void {
            trace(msg);
        }
        """
    ).strip()

    # Create two ActionScript files in different locations
    file_a = src_root / "main.as"
    file_b = src_root / "level1" / "helper.as"
    file_a.write_text(code)
    file_b.write_text(code)

    converter = FlashConverter()
    converter.convert_directory(src_root, dest_root)

    expected = textwrap.dedent(
        """
        let score = 0;
        function log(msg) {
            console.log(msg);
        }
        """
    ).strip()

    assert (dest_root / "main.js").read_text() == expected
    assert (dest_root / "level1" / "helper.js").read_text() == expected


def test_object_literals_and_defaults():
    src_code = textwrap.dedent(
        """
        var settings:Object = {foo: 1, bar: 2};
        function build(config:Object = {w:10, h:20}):Object {
            trace(config.w);
        }
        """
    ).strip()

    converter = FlashConverter()
    js = converter.convert_code(src_code)

    expected = textwrap.dedent(
        """
        let settings = {foo: 1, bar: 2};
        function build(config = {w:10, h:20}) {
            console.log(config.w);
        }
        """
    ).strip()

    assert js == expected
