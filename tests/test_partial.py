import inspect

from invoke import Context, task

from doctrine import partial


@task(help={"word": "Word to echo. Defaults to 'defaultword'."})
def reverse(c, word="defaultword"):
    """
    Echo the given word. Defaults to 'defaultword'.
    """
    return "".join(reversed(word))


reverse2 = partial(reverse)
reverse3 = partial(reverse, word="newdefault")


def test_name():
    assert reverse.name == reverse2.name


def test_params():
    assert inspect.signature(reverse.body) == inspect.signature(reverse2.body)
    assert inspect.getfullargspec(reverse.body) == inspect.getfullargspec(
        reverse2.body
    )


def test_help():
    assert reverse.help == reverse2.help


def test_calling():
    c = Context()
    assert reverse2(c) == reverse(c)


def test_calling2():
    c = Context()
    assert reverse3(c) == "tluafedwen"
