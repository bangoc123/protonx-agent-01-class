def print_welcome_banner():
    """Print a flashy welcome banner for A2A Protocol"""
    import os
    import time
    
    # Clear the terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # ANSI color codes
    class Colors:
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        PURPLE = '\033[95m'
        CYAN = '\033[96m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        END = '\033[0m'
    
    # Banner
    banner = f"""
    {Colors.BOLD}{Colors.BLUE}  █████╗ ██████╗  █████╗     ██████╗ ██████╗  ██████╗ ████████╗ ██████╗  ██████╗ ██████╗ ██╗     {Colors.END}
    {Colors.BOLD}{Colors.BLUE} ██╔══██╗╚════██╗██╔══██╗    ██╔══██╗██╔══██╗██╔═══██╗╚══██╔══╝██╔═══██╗██╔════╝██╔═══██╗██║     {Colors.END}
    {Colors.BOLD}{Colors.BLUE} ███████║ █████╔╝███████║    ██████╔╝██████╔╝██║   ██║   ██║   ██║   ██║██║     ██║   ██║██║     {Colors.END}
    {Colors.BOLD}{Colors.BLUE} ██╔══██║██╔═══╝ ██╔══██║    ██╔═══╝ ██╔══██╗██║   ██║   ██║   ██║   ██║██║     ██║   ██║██║     {Colors.END}
    {Colors.BOLD}{Colors.BLUE} ██║  ██║███████╗██║  ██║    ██║     ██║  ██║╚██████╔╝   ██║   ╚██████╔╝╚██████╗╚██████╔╝███████╗{Colors.END}
    {Colors.BOLD}{Colors.BLUE} ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝  ╚═════╝ ╚═════╝ ╚══════╝{Colors.END}
    """
    
    # Print banner with a typing effect
    for line in banner.split('\n'):
        print(line)
        time.sleep(0.1)  # Adjust for faster/slower typing effect
    
    # Print the divider
    divider = f"{Colors.YELLOW}{'═' * 100}{Colors.END}"
    print(divider)
    
    # Print welcome message
    welcome_message = [
        f"{Colors.BOLD}{Colors.GREEN}  Welcome to the A2A Protocol Interface{Colors.END}",
        f"{Colors.CYAN}  Portal: {Colors.UNDERLINE}https://a2aprotocol.network/dashboard{Colors.END}",
        f"{Colors.PURPLE}  © A2A Systems{Colors.END}",
        "",
        f"{Colors.YELLOW}  [+] {Colors.END}{Colors.BOLD}Protocol Information{Colors.END} - Learn about our secure communication standards",
        f"{Colors.YELLOW}  [+] {Colors.END}{Colors.BOLD}Network Status{Colors.END} - Check system uptime and performance metrics",
        f"{Colors.YELLOW}  [+] {Colors.END}Type {Colors.RED}'disconnect'{Colors.END} to terminate the secure session"
    ]
    
    # Print the welcome message with a typing effect
    for line in welcome_message:
        print(line)
        time.sleep(0.1)
    
    print(divider)
    print()
    print(f"{Colors.GREEN}Establishing secure connection...{Colors.END}")
    time.sleep(1)
    print(f"{Colors.GREEN}A2A Protocol is now active and ready!{Colors.END}")
    print()