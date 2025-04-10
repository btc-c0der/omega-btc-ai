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
    """Display a Matrix-like digital rain effect"""
    width = os.get_terminal_size().columns
    clear_screen()
    
    matrix_chars = "01ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｽﾀﾇﾍｦｲｸｺｿﾁﾄﾉﾌﾔﾖﾙﾚﾛﾝ1234567890"
    matrix_chars += "AIΦΩΣαβγδθλφπ∞≠≈§¶∫√∂≡±≤≥▲▼◄►"
    
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
                    # Highlight some characters in bright blue
                    line += f"\033[1;36m{matrix_chars[char_index]}\033[0m"
                else:
                    # Normal blue for most characters
                    line += f"\033[0;36m{matrix_chars[char_index]}\033[0m"
                
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

def draw_ai_logo():
    """Display the AI Future of Work logo"""
    logo = '''
     █████╗ ██╗    ███████╗██╗   ██╗████████╗██╗   ██╗██████╗ ███████╗
    ██╔══██╗██║    ██╔════╝██║   ██║╚══██╔══╝██║   ██║██╔══██╗██╔════╝
    ███████║██║    █████╗  ██║   ██║   ██║   ██║   ██║██████╔╝█████╗  
    ██╔══██║██║    ██╔══╝  ██║   ██║   ██║   ██║   ██║██╔══██╗██╔══╝  
    ██║  ██║██║    ██║     ╚██████╔╝   ██║   ╚██████╔╝██║  ██║███████╗
    ╚═╝  ╚═╝╚═╝    ╚═╝      ╚═════╝    ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝
    ███████╗██╗   ██╗████████╗██╗   ██╗██████╗ ███████╗     ██████╗ ███████╗    ██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗
    ██╔════╝██║   ██║╚══██╔══╝██║   ██║██╔══██╗██╔════╝    ██╔═══██╗██╔════╝    ██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝
    █████╗  ██║   ██║   ██║   ██║   ██║██████╔╝█████╗      ██║   ██║█████╗      ██║ █╗ ██║██║   ██║██████╔╝█████╔╝ 
    ██╔══╝  ██║   ██║   ██║   ██║   ██║██╔══██╗██╔══╝      ██║   ██║██╔══╝      ██║███╗██║██║   ██║██╔══██╗██╔═██╗ 
    ██║     ╚██████╔╝   ██║   ╚██████╔╝██║  ██║███████╗    ╚██████╔╝██║         ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗
    ╚═╝      ╚═════╝    ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝     ╚═════╝ ╚═╝          ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
    '''
    
    # Animate with colors
    colors = ['\033[36m', '\033[1;36m', '\033[34m', '\033[1;34m', '\033[35m', '\033[1;35m']
    for i in range(6):
        clear_screen()
        print(f"{colors[i % len(colors)]}{logo}\033[0m")
        time.sleep(0.15)
    
    # Final logo in bright cyan
    clear_screen()
    print(f"\033[1;36m{logo}\033[0m")
    time.sleep(0.5)

def draw_border(text, color="\033[1;36m"):
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

def draw_progress_bar(title, delay=0.05):
    """Draw an animated progress bar"""
    width = 40
    print(f"\n{title}:")
    sys.stdout.write("│")
    sys.stdout.flush()
    
    for i in range(width):
        time.sleep(delay)
        sys.stdout.write("█")
        sys.stdout.flush()
    
    sys.stdout.write("│ 100%\n")
    sys.stdout.flush()

def draw_human_ai_collaboration():
    """Draw animated human-AI collaboration visualization"""
    frames = [
        '''
            🧠       ⚙️        👤
           HUMAN     AI      FUTURE
             \\      |       /
              \\     |      /
               \\    |     /
                \\   |    /
                 \\  |   /
                  \\ |  /
                   \\| /
                    ⟱
              COLLABORATION
                    |
                    |
                    ⟱
               INNOVATION
        ''',
        '''
            🧠       ⚙️        👤
           HUMAN     AI      FUTURE
              \\     |      /
               \\    |     /
                \\   |    /
                 \\  |   /
                  \\ |  /
                   \\|/
                    ⟱
              COLLABORATION
                    |
                    ⟱
               INNOVATION
                    |
              TRANSFORMATION
        '''
    ]
    
    for _ in range(3):
        for frame in frames:
            clear_screen()
            print("\033[1;35m", end="")  # Magenta
            print(frame)
            print("\033[0m", end="")
            time.sleep(0.5)

def animate_industries():
    """Animate industries being transformed by AI"""
    industries = [
        "HEALTHCARE", "FINANCE", "EDUCATION", "MANUFACTURING",
        "RETAIL", "TRANSPORTATION", "CREATIVE ARTS", "AGRICULTURE"
    ]
    
    clear_screen()
    print("\033[1;33m╭" + "─" * 50 + "╮\033[0m")
    print("\033[1;33m│" + " INDUSTRIES BEING TRANSFORMED BY AI ".center(50) + "│\033[0m")
    print("\033[1;33m╰" + "─" * 50 + "╯\033[0m\n")
    
    for industry in industries:
        sys.stdout.write("\033[1;32m> \033[0m")
        sys.stdout.flush()
        time.sleep(0.2)
        
        for char in industry:
            sys.stdout.write(f"\033[1;37m{char}\033[0m")
            sys.stdout.flush()
            time.sleep(0.05)
        
        time.sleep(0.1)
        sys.stdout.write("\033[1;32m ✓\033[0m\n")
        sys.stdout.flush()
        time.sleep(0.3)

def display_job_evolution():
    """Display job evolution animation"""
    job_evolution = [
        ("OLD JOB", "NEW JOB"),
        ("Data Entry", "Data Strategy Specialist"),
        ("Customer Service Rep", "Customer Experience Architect"),
        ("Factory Worker", "Automation Supervisor"),
        ("Financial Analyst", "AI-Finance Integration Expert"),
        ("Medical Transcriptionist", "Clinical AI Trainer"),
        ("Journalist", "Narrative AI Curator"),
        ("Software Tester", "AI Testing Ethics Manager"),
        ("Marketing Manager", "Human-AI Marketing Orchestrator")
    ]
    
    clear_screen()
    print("\033[1;34m╭" + "─" * 60 + "╮\033[0m")
    print("\033[1;34m│" + " JOB EVOLUTION IN THE AGE OF AI ".center(60) + "│\033[0m")
    print("\033[1;34m╰" + "─" * 60 + "╯\033[0m\n")
    
    # Print table header
    print("\033[1;37m{:<30} {:<30}\033[0m".format(job_evolution[0][0], job_evolution[0][1]))
    print("─" * 60)
    
    # Print each job transformation with animation
    for old_job, new_job in job_evolution[1:]:
        print("\033[0;37m{:<30}\033[0m".format(old_job), end="")
        sys.stdout.flush()
        time.sleep(0.3)
        
        print(" \033[1;36m{:<30}\033[0m".format(new_job))
        sys.stdout.flush()
        time.sleep(0.5)

def display_ai_impact_chart():
    """Display a chart showing AI impact on work"""
    chart = '''
    AI IMPACT ON WORK (2025-2035)
    
    AUTOMATION     ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉░░░░░ 75%
    AUGMENTATION   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉░░ 90% 
    NEW JOBS       ▉▉▉▉▉▉▉▉▉▉▉▉▉▉░░░░░░ 70%
    PRODUCTIVITY   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉░░░ 85%
    CREATIVITY     ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉░░░░ 80%
    DECISION-MAKING▉▉▉▉▉▉▉▉▉▉▉▉▉░░░░░░░ 65%
    
    ░ = Current level   ▉ = Projected growth
    '''
    
    clear_screen()
    print("\033[1;33m", end="")
    print_with_typing(chart, delay=0.005)
    print("\033[0m", end="")
    time.sleep(1)

def display_ai_work_future():
    """Main function to display the future of AI in work"""
    clear_screen()
    
    # Matrix rain effect
    matrix_rain(duration=2.0, speed=0.03)
    
    # Display logo
    draw_ai_logo()
    time.sleep(0.5)
    
    # Introduction
    intro_text = '''
    HOW ARTIFICIAL INTELLIGENCE WILL SHAPE THE FUTURE OF WORK
    
    AI is poised to fundamentally transform how we work, what we work on,
    and the skills we need to thrive in the coming decades.
    '''
    draw_border(intro_text)
    time.sleep(1)
    
    # Show human-AI collaboration
    draw_human_ai_collaboration()
    
    # Key trends
    trends_text = '''
    KEY TRENDS IN AI AND WORK
    
    1. AUTOMATION OF ROUTINE TASKS
       Repetitive and predictable work will be increasingly automated,
       freeing humans to focus on creative and strategic activities.
    
    2. HUMAN-AI COLLABORATION
       The most effective workplaces will blend human creativity and
       empathy with AI efficiency and analytical power.
    
    3. CONTINUOUS LEARNING
       Workers will need to constantly adapt skills as AI evolves,
       with emphasis on uniquely human capabilities.
    
    4. NEW JOB CATEGORIES
       AI will create entirely new roles that don't exist today,
       focused on managing, training, and working alongside AI.
    
    5. DISTRIBUTED WORK
       AI tools will enable more effective remote collaboration
       and breakdown geographic barriers to talent.
    '''
    clear_screen()
    draw_border(trends_text, color="\033[1;32m")
    time.sleep(2)
    
    # Animation of industries
    animate_industries()
    time.sleep(1)
    
    # Progress bar animations
    clear_screen()
    draw_progress_bar("AI INTEGRATION ACROSS INDUSTRIES", 0.03)
    draw_progress_bar("WORKFORCE ADAPTATION TO AI", 0.03)
    draw_progress_bar("DEVELOPMENT OF AI REGULATION", 0.03)
    time.sleep(0.5)
    
    # Job evolution
    display_job_evolution()
    time.sleep(1)
    
    # Impact chart
    display_ai_impact_chart()
    time.sleep(1)
    
    # Conclusion
    conclusion_text = '''
    THE FUTURE OF WORK WITH AI

    The integration of AI into the workplace won't be about
    replacing humans, but about redefining human potential.
    
    The most successful organizations will be those that find
    the right balance between artificial intelligence and
    human intelligence, creating environments where both can
    thrive and complement each other's strengths.
    
    As AI handles more routine cognitive tasks, human work
    will increasingly focus on creativity, critical thinking,
    emotional intelligence, and ethical judgment - areas where
    humans continue to excel.
    
    The future of work is not HUMAN VS. AI, but HUMAN AND AI.
    '''
    clear_screen()
    draw_border(conclusion_text, color="\033[1;35m")
    
    # Final matrix rain
    time.sleep(2)
    matrix_rain(duration=1.5, speed=0.03)
    
    # Final message
    final_message = "\n\033[1;36m✧✧✧ AI FUTURE OF WORK VISUALIZATION COMPLETE ✧✧✧\033[0m"
    print(final_message)

if __name__ == "__main__":
    try:
        display_ai_work_future()
    except KeyboardInterrupt:
        clear_screen()
        print("\n\033[1;31mVisualization interrupted. Exiting...\033[0m")
    except Exception as e:
        print(f"\n\033[1;31mError in visualization: {e}\033[0m") 