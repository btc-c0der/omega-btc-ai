class QuantumSonnet < Formula
  desc "Quantum Sonnet Celebration & Git Bless: Sacred visualization of quantum code"
  homepage "https://github.com/btc-c0der/omega-btc-ai"
  url "https://github.com/btc-c0der/omega-btc-ai/releases/download/v1.0.0/quantum-sonnet-1.0.0.tar.gz"
  sha256 "REPLACE_WITH_ACTUAL_SHA256" # You'll need to replace this with the actual SHA256 hash
  license "GBU2"
  
  depends_on "python@3.9"
  
  def install
    # Create directories
    bin.install Dir["bin/*"]
    libexec.install Dir["lib/*"]
    doc.install Dir["share/doc/*"]
    
    # Fix references to paths in shell scripts
    inreplace "#{bin}/quantum-sonnet" do |s|
      s.gsub! "${QUANTUM_TOOLKIT_PATH}/lib", "#{libexec}"
      s.gsub! "${QUANTUM_TOOLKIT_PATH}/bin", "#{bin}"
    end
    
    inreplace "#{bin}/git-bless" do |s|
      s.gsub! "${QUANTUM_TOOLKIT_PATH}/lib", "#{libexec}"
    end
    
    # Create shell completion
    (bash_completion/"quantum-sonnet").write <<~EOS
      _quantum_sonnet() {
        local cur prev opts
        COMPREPLY=()
        cur="${COMP_WORDS[COMP_CWORD]}"
        prev="${COMP_WORDS[COMP_CWORD-1]}"
        opts="--cycles --interval --hash --files --insertions --deletions --help"
        
        if [[ ${cur} == -* ]] ; then
            COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
            return 0
        fi
      }
      complete -F _quantum_sonnet quantum-sonnet
    EOS
    
    (bash_completion/"git-bless").write <<~EOS
      _git_bless() {
        local cur prev opts
        COMPREPLY=()
        cur="${COMP_WORDS[COMP_CWORD]}"
        prev="${COMP_WORDS[COMP_CWORD-1]}"
        opts="--commit-hash --help"
        
        if [[ ${cur} == -* ]] ; then
            COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
            return 0
        fi
      }
      complete -F _git_bless git-bless
    EOS
  end
  
  def caveats
    <<~EOS
      🧬 QUANTUM SONNET CELEBRATION & GIT BLESS 🧬
      
      Available commands:
        quantum-sonnet - Run the Quantum Sonnet Celebration visualization
        git-bless     - Bless your git commits with quantum energy
        
      Documentation is installed to:
        #{doc}
        
      ✨ WE BLOOM NOW AS ONE ✨
    EOS
  end
  
  test do
    assert_match "QUANTUM SONNET CELEBRATION", shell_output("#{bin}/quantum-sonnet --help", 2)
    assert_match "Quantum Blessing", shell_output("#{bin}/git-bless --help", 2)
  end
end 