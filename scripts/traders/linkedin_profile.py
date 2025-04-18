#!/usr/bin/env python3
import time
import random
import os
import sys
from datetime import datetime

def clear_screen():
    """Clear the terminal screen based on OS"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_with_typing(text, delay=0.02):
    """Print text with a typing effect"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def matrix_rain(duration=2.0, speed=0.05):
    """Display a Matrix-like digital rain effect with LinkedIn-related terms"""
    width = os.get_terminal_size().columns
    clear_screen()
    
    matrix_chars = "01ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｽﾀﾇﾍｦｲｸｺｿﾁﾄﾉﾌﾔﾖﾙﾚﾛﾝ1234567890"
    matrix_chars += "AIBlockchainLeadershipInnovationQuantumBTCNFTCreativeDirectorAnalyticsPythonDev"
    
    columns = {}
    for i in range(width):
        columns[i] = -1
    
    start_time = time.time()
    while time.time() - start_time < duration:
        line = ""
        for i in range(width):
            if columns[i] >= 0:
                char_index = random.randint(0, len(matrix_chars) - 1)
                if i % 3 == 0 and random.random() > 0.8:
                    # Highlight some characters in bright blue (LinkedIn color)
                    line += f"\033[1;34m{matrix_chars[char_index]}\033[0m"
                else:
                    # Normal blue for most characters
                    line += f"\033[0;34m{matrix_chars[char_index]}\033[0m"
                
                columns[i] += 1
                if columns[i] > random.randint(5, 15):
                    columns[i] = -1
            else:
                if random.random() > 0.95:
                    columns[i] = 0
                line += " "
        
        print(line)
        time.sleep(speed)
    
    clear_screen()

def draw_linkedin_logo():
    """Display the LinkedIn logo and profile header"""
    logo = '''
    ██╗     ██╗███╗   ██╗██╗  ██╗███████╗██████╗ ██╗███╗   ██╗
    ██║     ██║████╗  ██║██║ ██╔╝██╔════╝██╔══██╗██║████╗  ██║
    ██║     ██║██╔██╗ ██║█████╔╝ █████╗  ██║  ██║██║██╔██╗ ██║
    ██║     ██║██║╚██╗██║██╔═██╗ ██╔══╝  ██║  ██║██║██║╚██╗██║
    ███████╗██║██║ ╚████║██║  ██╗███████╗██████╔╝██║██║ ╚████║
    ╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝╚═╝  ╚═══╝
    ██████╗ ██████╗  ██████╗ ███████╗██╗██╗     ███████╗
    ██╔══██╗██╔══██╗██╔═══██╗██╔════╝██║██║     ██╔════╝
    ██████╔╝██████╔╝██║   ██║█████╗  ██║██║     █████╗  
    ██╔═══╝ ██╔══██╗██║   ██║██╔══╝  ██║██║     ██╔══╝  
    ██║     ██║  ██║╚██████╔╝██║     ██║███████╗███████╗
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚══════╝
    https://www.linkedin.com/in/faustocsiqueira/
    '''
    
    # Animate with LinkedIn blue colors
    colors = ['\033[34m', '\033[1;34m', '\033[38;5;27m', '\033[38;5;33m']
    for i in range(6):
        clear_screen()
        print(f"{colors[i % len(colors)]}{logo}\033[0m")
        time.sleep(0.15)
    
    # Final logo in LinkedIn blue
    clear_screen()
    print(f"\033[38;5;27m{logo}\033[0m")
    time.sleep(0.8)

def draw_border(text, color="\033[38;5;27m"):
    """Draw a border around text"""
    lines = text.split('\n')
    max_length = max(len(line) for line in lines)
    
    top_border = '╭' + '─' * (max_length + 2) + '╮'
    bottom_border = '╰' + '─' * (max_length + 2) + '╯'
    
    bordered_text = [top_border]
    for line in lines:
        if line.strip():
            bordered_text.append('│ ' + line.ljust(max_length) + ' │')
        else:
            bordered_text.append('│' + ' ' * (max_length + 2) + '│')
    bordered_text.append(bottom_border)
    
    # Animate border drawing
    print(color, end="")
    for line in bordered_text:
        print_with_typing(line, delay=0.005)
    print("\033[0m", end="")

def show_profile_summary():
    """Show profile summary with animated typing"""
    summary = '''
    FAUSTO SIQUEIRA
    Quantum-Blockchain Creative Director & AI Innovation Leader
    
    Pioneering the intersection of quantum computing, blockchain, and artificial intelligence
    to create transformative digital experiences and advanced technological solutions.
    
    🌐 Sao Paulo, Brazil  |  🔗 https://www.linkedin.com/in/faustocsiqueira/
    '''
    
    clear_screen()
    print("\033[1;38;5;33m", end="")  # LinkedIn blue, bold
    print_with_typing(summary, delay=0.02)
    print("\033[0m")
    time.sleep(1.5)

def animate_skills_graph():
    """Animate a skills graph visualization"""
    skills = [
        ("Blockchain Development", 95),
        ("AI & Machine Learning", 92),
        ("Quantum Computing", 88),
        ("Creative Direction", 96),
        ("Python Development", 94),
        ("Leadership & Strategy", 90),
        ("NFT & Digital Assets", 98),
        ("UI/UX & Design", 85)
    ]
    
    clear_screen()
    print("\n\033[1;38;5;27m╭" + "─" * 50 + "╮\033[0m")
    print("\033[1;38;5;27m│" + " PROFESSIONAL SKILLS & EXPERTISE ".center(50) + "│\033[0m")
    print("\033[1;38;5;27m╰" + "─" * 50 + "╯\033[0m\n")
    
    for skill, percentage in skills:
        # Create the bar
        bar_length = 40
        filled_length = int(bar_length * percentage / 100)
        
        print(f"\033[1;38;5;27m{skill}:\033[0m")
        sys.stdout.write("│")
        
        # Animate the progress bar
        for i in range(bar_length):
            time.sleep(0.01)
            if i < filled_length:
                # Gradient coloring from blue to cyan
                color_val = 27 + int((i / filled_length) * 6)
                sys.stdout.write(f"\033[38;5;{color_val}m█\033[0m")
            else:
                sys.stdout.write("░")
            sys.stdout.flush()
        
        sys.stdout.write(f"│ {percentage}%\n\n")
        sys.stdout.flush()
        time.sleep(0.2)
    
    time.sleep(1)

def show_experience():
    """Show professional experience with animated sections"""
    experiences = [
        {
            "title": "🌟 QUANTUM BLOCKCHAIN CREATIVE DIRECTOR",
            "company": "OMEGA Technologies",
            "period": "2021 - Present",
            "description": [
                "• Leading innovative blockchain solutions with quantum-resistant architectures",
                "• Directing creative strategies for NFT marketplaces and digital asset platforms",
                "• Pioneering AI integration in distributed ledger technologies",
                "• Managing cross-functional teams across multiple projects"
            ]
        },
        {
            "title": "🚀 AI INNOVATION STRATEGIST",
            "company": "Future Systems Institute",
            "period": "2018 - 2021",
            "description": [
                "• Developed AI-driven solutions for financial forecasting and market analysis",
                "• Implemented machine learning algorithms for predictive analytics",
                "• Created automated trading systems with advanced pattern recognition",
                "• Led workshops on emerging AI technologies and implementation strategies"
            ]
        },
        {
            "title": "💻 SENIOR BLOCKCHAIN DEVELOPER",
            "company": "Distributed Systems Technologies",
            "period": "2015 - 2018",
            "description": [
                "• Architected and developed enterprise blockchain solutions",
                "• Created smart contract systems for decentralized applications",
                "• Implemented security protocols for cryptocurrency exchanges",
                "• Contributed to open-source blockchain projects and standards"
            ]
        }
    ]
    
    for exp in experiences:
        clear_screen()
        
        # Title and company
        print(f"\n\033[1;38;5;33m{exp['title']}\033[0m")
        print(f"\033[1;37m{exp['company']} | {exp['period']}\033[0m")
        print("─" * 60)
        
        # Animate description points
        for point in exp["description"]:
            print_with_typing(f"\033[38;5;27m{point}\033[0m", delay=0.02)
            time.sleep(0.3)
        
        print("\n")
        time.sleep(1.5)

def show_projects():
    """Display notable projects with animations"""
    projects = [
        {
            "title": "🔮 OMEGA-BTC-AI",
            "description": "A quantum-resistant blockchain system with integrated AI for cryptocurrency market prediction and NFT generation",
            "technologies": ["Python", "TensorFlow", "Blockchain", "Quantum Algorithms"]
        },
        {
            "title": "🎨 DIVINE DASHBOARD",
            "description": "Advanced visualization platform for blockchain analytics with creative AI-generated representations of market data",
            "technologies": ["JavaScript", "D3.js", "React", "Node.js", "WebGL"]
        },
        {
            "title": "🧠 NEURAL PROPHECY ENGINE",
            "description": "Innovative AI system that combines market data with creative algorithms to generate predictive visualizations",
            "technologies": ["Python", "PyTorch", "CUDA", "FastAPI"]
        }
    ]
    
    clear_screen()
    print("\n\033[1;38;5;27m╭" + "─" * 50 + "╮\033[0m")
    print("\033[1;38;5;27m│" + " NOTABLE PROJECTS ".center(50) + "│\033[0m")
    print("\033[1;38;5;27m╰" + "─" * 50 + "╯\033[0m\n")
    
    for project in projects:
        # Show project title with typing animation
        print_with_typing(f"\033[1;38;5;33m{project['title']}\033[0m", delay=0.02)
        time.sleep(0.2)
        
        # Show project description
        print_with_typing(f"\033[38;5;27m{project['description']}\033[0m", delay=0.01)
        time.sleep(0.3)
        
        # Show technologies with animation
        sys.stdout.write("\033[38;5;240mTechnologies: \033[0m")
        sys.stdout.flush()
        
        for i, tech in enumerate(project['technologies']):
            time.sleep(0.2)
            if i > 0:
                sys.stdout.write(" • ")
                sys.stdout.flush()
            sys.stdout.write(f"\033[1;38;5;33m{tech}\033[0m")
            sys.stdout.flush()
        
        print("\n" + "─" * 60 + "\n")
        time.sleep(0.5)
    
    time.sleep(1)

def show_recommendations():
    """Show animated recommendations from professionals"""
    recommendations = [
        {
            "name": "Dr. Sophia Chen",
            "position": "Chief Technology Officer, Quantum Solutions Inc.",
            "text": "\"Fausto brings a rare combination of technical expertise and creative vision. His work in quantum-resistant blockchain systems has been groundbreaking, and his leadership continues to inspire innovation across multiple domains.\""
        },
        {
            "name": "Marcus Williams",
            "position": "Director of AI Research, Global Analytics Partners",
            "text": "\"Working with Fausto was transformative for our AI initiatives. His deep understanding of both the technical and creative aspects of artificial intelligence helped us develop solutions that were not only functional but visionary.\""
        },
        {
            "name": "Elena Rodriguez",
            "position": "Founder & CEO, NextGen Blockchain Ventures",
            "text": "\"Fausto's contributions to blockchain technology have been exceptional. His ability to bridge quantum computing concepts with practical blockchain applications is unparalleled in the industry.\""
        }
    ]
    
    clear_screen()
    print("\n\033[1;38;5;27m" + "✨ RECOMMENDATIONS & ENDORSEMENTS ✨".center(60) + "\033[0m\n")
    
    for rec in recommendations:
        print("\033[38;5;240m❝\033[0m")
        print_with_typing(f"\033[38;5;27m{rec['text']}\033[0m", delay=0.01)
        print("\033[38;5;240m❞\033[0m\n")
        
        time.sleep(0.3)
        print_with_typing(f"\033[1;38;5;33m— {rec['name']}\033[0m", delay=0.02)
        print_with_typing(f"\033[38;5;240m   {rec['position']}\033[0m", delay=0.02)
        print("\n" + "─" * 60 + "\n")
        time.sleep(1)
    
    time.sleep(0.5)

def show_contact_info():
    """Show contact information with animated icons"""
    contact_info = '''
    CONNECT WITH ME
    
    📧 email@example.com
    🔗 linkedin.com/in/faustocsiqueira
    🌐 professional-website.com
    🐦 @twitter_handle
    
    Open to opportunities in:
    • Quantum-Blockchain Innovation
    • AI Creative Direction
    • Technology Leadership
    • Strategic Consulting
    '''
    
    clear_screen()
    draw_border(contact_info, color="\033[1;38;5;33m")
    time.sleep(2)

def show_achievements():
    """Show professional achievements with animated icons"""
    achievements = [
        "🏆 Blockchain Innovation Award, Global Tech Summit 2023",
        "📚 Author, 'Quantum Futures: The Convergence of Blockchain & AI'",
        "🎓 Guest Lecturer, MIT Technology Leadership Program",
        "💡 15+ Patents in Blockchain & AI Technologies",
        "🔑 Keynote Speaker at Web3 Conference 2022",
        "🌟 Featured in 'Top 40 Under 40 Tech Leaders'"
    ]
    
    clear_screen()
    print("\n\033[1;38;5;27m╭" + "─" * 50 + "╮\033[0m")
    print("\033[1;38;5;27m│" + " ACHIEVEMENTS & RECOGNITION ".center(50) + "│\033[0m")
    print("\033[1;38;5;27m╰" + "─" * 50 + "╯\033[0m\n")
    
    for achievement in achievements:
        print_with_typing(f"\033[38;5;27m{achievement}\033[0m", delay=0.02)
        time.sleep(0.5)
    
    time.sleep(1.5)

def display_qr_code():
    """Display a LinkedIn QR code in ASCII art"""
    qr_code = '''
          ██████████████      ████  ████████████
          ██          ██    ██  ████  ██      ██
          ██  ██████  ██  ████      ████  ██  ██
          ██  ██████  ██  ██  ██  ██  ██      ██
          ██  ██████  ██  ██  ██    ████  ██████
          ██          ██  ████    ██  ████  ████
          ██████████████  ██  ██  ██  ██  ██  ██
                          ██████  ██████  ██  ██
          ██  ██  ██  ██      ██████    ████  ██
          ████  ████  ██████  ██  ██    ████████
            ██████  ██    ██  ████  ██        ██
          ██████    ██    ██    ██████    ██  ██
                ██    ██  ██  ██  ████  ██    ██
                          ██  ██  ██  ██  ██████
          ██████████████  ██    ████  ██████  ██
          ██          ██  ██████  ██████  ██  ██
          ██  ██████  ██  ████        ██      ██
          ██  ██████  ██    ██    ████  ██  ████
          ██  ██████  ██  ██    ██    ██  ██  ██
          ██          ██  ██████  ██    ████  ██
          ██████████████  ██  ██  ██████  ██  ██
          
          Scan to visit my LinkedIn profile
          linkedin.com/in/faustocsiqueira
    '''
    
    clear_screen()
    print("\033[1;38;5;27m", end="")  # LinkedIn blue
    print(qr_code)
    print("\033[0m")
    time.sleep(2.5)

def display_linkedin_profile():
    """Main function to display LinkedIn profile"""
    try:
        clear_screen()
        
        # Start with matrix rain
        matrix_rain(duration=1.5, speed=0.03)
        
        # Show LinkedIn logo
        draw_linkedin_logo()
        time.sleep(0.5)
        
        # Profile summary
        show_profile_summary()
        
        # Skills graph
        animate_skills_graph()
        
        # Professional experience
        show_experience()
        
        # Projects
        show_projects()
        
        # Achievements
        show_achievements()
        
        # Recommendations
        show_recommendations()
        
        # Contact information
        show_contact_info()
        
        # QR Code
        display_qr_code()
        
        # Final matrix rain
        matrix_rain(duration=1.5, speed=0.03)
        
        # Final message
        clear_screen()
        final_message = "\n\033[1;38;5;33m✧✧✧ CONNECT WITH ME ON LINKEDIN! ✧✧✧\033[0m"
        print(final_message)
        print("\n\033[1;38;5;27mhttps://www.linkedin.com/in/faustocsiqueira/\033[0m\n")
        
    except KeyboardInterrupt:
        clear_screen()
        print("\n\033[1;31mProfile visualization interrupted. Exiting...\033[0m")
    except Exception as e:
        print(f"\n\033[1;31mError in profile visualization: {e}\033[0m")

if __name__ == "__main__":
    display_linkedin_profile() 