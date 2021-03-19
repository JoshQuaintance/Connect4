import chalk


def err(message: str, end: str = '\n'):
    print(chalk.red(message, bold=True), end=end)


def warn(message: str, end: str = '\n'):
    print(chalk.yellow(f'WARN ~ {message}'), end=end)


def good(message: str, end: str = '\n'):
    print(chalk.green(f'{message}'), end=end)


def info(message: str, end: str = '\n'):
    print(chalk.blue(f'{message}'), end=end)
