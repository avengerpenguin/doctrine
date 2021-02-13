from textwrap import dedent

from invoke import Collection
from invoke import Program as Programme
from invoke import task

from doctrine import add_task


@task
def foo(c):
    print("foo")


@task
def echo(c, word):
    """
    Echo the given word.
    """
    print(word)


@task(help={"word": "Word to echo. Defaults to 'defaultword'."})
def default(c, word="defaultword"):
    """
    Echo the given word. Defaults to 'defaultword'.
    """
    print(word)


def myapp():
    ns = Collection()
    add_task(ns, foo)
    add_task(ns, echo)
    add_task(ns, default)
    return ns


def xtest_help(capsys):
    programme = Programme(namespace=myapp())
    assert default.help == programme.namespace["default"].help
    programme.run("invoke --help", exit=False)
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == dedent(
        """\
        Usage: invoke [--core-opts] <subcommand> [--subcommand-opts] ...

        Core options:

          --complete                         Print tab-completion candidates for given
                                             parse remainder.
          --hide=STRING                      Set default value of run()'s 'hide' kwarg.
          --print-completion-script=STRING   Print the tab-completion script for your
                                             preferred shell (bash|zsh|fish).
          --prompt-for-sudo-password         Prompt user at start of session for the
                                             sudo.password config value.
          --write-pyc                        Enable creation of .pyc files.
          -d, --debug                        Enable debug output.
          -D INT, --list-depth=INT           When listing tasks, only show the first
                                             INT levels.
          -e, --echo                         Echo executed commands before running.
          -f STRING, --config=STRING         Runtime configuration file to use.
          -F STRING, --list-format=STRING    Change the display format used when
                                             listing tasks. Should be one of: flat
                                             (default), nested, json.
          -h [STRING], --help[=STRING]       Show core or per-task help and exit.
          -l [STRING], --list[=STRING]       List available tasks, optionally limited
                                             to a namespace.
          -p, --pty                          Use a pty when executing shell commands.
          -R, --dry                          Echo commands instead of running.
          -T INT, --command-timeout=INT      Specify a global command execution
                                             timeout, in seconds.
          -V, --version                      Show version and exit.
          -w, --warn-only                    Warn, instead of failing, when shell
                                             commands fail.

        Subcommands:

          default   Echo the given word. Defaults to 'defaultword'.
          echo      Echo the given word.
          foo

        """
    )


def test_task_with_no_args(capsys):
    programme = Programme(namespace=myapp())
    programme.run("invoke foo", exit=False)
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == "foo\n"


def test_task_with_no_args_help(capsys):
    programme = Programme(namespace=myapp())
    programme.run("invoke foo -h", exit=False)
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == dedent(
        """\
        Usage: invoke [--core-opts] foo [other tasks here ...]

        Docstring:
          none

        Options:
          none

        """
    )


def test_task_with_one_arg(capsys):
    programme = Programme(namespace=myapp())
    programme.run("invoke echo bar", exit=False)
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == "bar\n"


def test_task_with_one_arg_not_given(capsys):
    programme = Programme(namespace=myapp())
    programme.run("invoke echo", exit=False)
    captured = capsys.readouterr()
    assert (
        captured.err
        == "'echo' did not receive required positional arguments: 'word'\n"
    )
    assert captured.out == ""


def test_task_with_one_arg_help(capsys):
    programme = Programme(namespace=myapp())
    programme.run("invoke --help echo", exit=False)
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == dedent(
        """\
        Usage: invoke [--core-opts] echo [--options] [other tasks here ...]

        Docstring:
          Echo the given word.

        Options:
          -w STRING, --word=STRING

        """
    )


def test_task_with_one_kw_arg_not_given(capsys):
    programme = Programme(namespace=myapp())
    programme.run("invoke default", exit=False)
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == "defaultword\n"


def test_app_setting_different_default(capsys):
    def myapp2():
        ns = Collection()
        add_task(ns, default, word="appdefault")
        return ns

    programme = Programme(namespace=myapp2())
    programme.run("invoke default", exit=False)
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == "appdefault\n"
