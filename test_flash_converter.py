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


def test_const_and_semicolonless_trace():
    src_code = textwrap.dedent(
        """
        const PI:Number = 3.14;
        function show(items:Vector.<String>):void {
            trace(items[0])
        }
        """
    ).strip()

    converter = FlashConverter()
    js = converter.convert_code(src_code)

    expected = textwrap.dedent(
        """
        const PI = 3.14;
        function show(items) {
            console.log(items[0])
        }
        """
    ).strip()

    assert js == expected


def test_trace_with_space_before_parens():
    src_code = textwrap.dedent(
        """
        trace ('a');
        trace  ('b');
        trace\t('c');
        """
    ).strip()

    converter = FlashConverter()
    js = converter.convert_code(src_code)

    expected = textwrap.dedent(
        """
        console.log('a');
        console.log('b');
        console.log('c');
        """
    ).strip()

    assert js == expected


def test_trace_not_part_of_identifier_or_method():
    src_code = textwrap.dedent(
        """
        mytrace('a');
        logger.trace('b');
        trace('c');
        """
    ).strip()

    converter = FlashConverter()
    js = converter.convert_code(src_code)

    expected = textwrap.dedent(
        """
        mytrace('a');
        logger.trace('b');
        console.log('c');
        """
    ).strip()

    assert js == expected


def test_package_and_import_removal():
    src_code = textwrap.dedent(
        """
        package {
            import flash.utils.Dictionary;
            var count:int = 0;
            function inc(val:int):void {
                trace(val);
            }
        }
        """
    ).strip()

    converter = FlashConverter()
    js = converter.convert_code(src_code)

    expected = textwrap.dedent(
        """
        let count = 0;
        function inc(val) {
            console.log(val);
        }
        """
    ).strip()

    assert js == expected


def test_access_modifiers_removed():
    src_code = textwrap.dedent(
        """
        public var score:int = 0;
        private const PI:Number = 3.14;
        protected function inc(val:int):void {
            trace(val);
        }
        static function count():int {
            return 0;
        }
        """
    ).strip()

    converter = FlashConverter()
    js = converter.convert_code(src_code)

    expected = textwrap.dedent(
        """
        let score = 0;
        const PI = 3.14;
        function inc(val) {
            console.log(val);
        }
        function count() {
            return 0;
        }
        """
    ).strip()

    assert js == expected


def test_for_each_loop_conversion():
    src_code = textwrap.dedent(
        """
        var items:Array = [1, 2, 3];
        for each (var item in items) {
            trace(item);
        }
        """
    ).strip()

    converter = FlashConverter()
    js = converter.convert_code(src_code)

    expected = textwrap.dedent(
        """
        let items = [1, 2, 3];
        for (let item of items) {
            console.log(item);
        }
        """
    ).strip()

    assert js == expected


def test_class_implements_removed():
    src_code = textwrap.dedent(
        """
        public class MySprite extends Sprite implements IFoo, IBar {
            public function MySprite() {
                trace('hi');
            }
        }

        internal class Simple implements IThing {
            public function Simple() {
                trace('x');
            }
        }
        """
    ).strip()

    converter = FlashConverter()
    js = converter.convert_code(src_code)

    expected = textwrap.dedent(
        """
        class MySprite extends Sprite {
            function MySprite() {
                console.log('hi');
            }
        }

        class Simple {
            function Simple() {
                console.log('x');
            }
        }
        """
    ).strip()

    assert js == expected
