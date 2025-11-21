import math
import collections
import os
import random

def calculate_entropy(file_path):
    """
    Calculate information entropy of a file
    """
    try:
        # Read file in binary mode to handle all file types
        with open(file_path, 'rb') as file:
            data = file.read()
        
        if len(data) == 0:
            return 0.0
        
        # Count byte frequencies
        byte_counts = collections.Counter(data)
        total_bytes = len(data)
        
        # Calculate entropy
        entropy = 0.0
        for count in byte_counts.values():
            # Probability of this byte
            p_x = count / total_bytes
            # Entropy contribution
            entropy -= p_x * math.log2(p_x)
        
        return entropy
    
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def generate_test_files():
    """
    Generate test files as specified in the assignment
    """
    # File 1: All identical characters (should have entropy ~0)
    with open('identical_chars.txt', 'w') as f:
        f.write('A' * 1000)
    
    # File 2: Random 0 and 1 (binary)
    with open('random_binary.txt', 'w') as f:
        binary_data = ''.join(random.choice('01') for _ in range(1000))
        f.write(binary_data)
    
    # File 3: Random bytes 0-255
    with open('random_bytes.bin', 'wb') as f:
        random_bytes = bytes(random.randint(0, 255) for _ in range(1000))
        f.write(random_bytes)
    
    # File 4: Text with medium entropy
    with open('medium_entropy.txt', 'w') as f:
        text = "This is a sample text with medium entropy level. " * 20
        f.write(text)

def main():
    """
    Main function to demonstrate the program
    """
    print("=== File Entropy Calculator ===\n")
    
    # Generate test files
    print("Generating test files...")
    generate_test_files()
    print("Test files created!\n")
    
    # Calculate entropy for each file
    test_files = [
        'identical_chars.txt',
        'random_binary.txt', 
        'random_bytes.bin',
        'medium_entropy.txt'
    ]
    
    print("Calculating entropy:")
    print("-" * 50)
    
    for file_name in test_files:
        if os.path.exists(file_name):
            entropy = calculate_entropy(file_name)
            file_size = os.path.getsize(file_name)
            
            print(f"File: {file_name:20} | Size: {file_size:4} bytes | Entropy: {entropy:.4f} bits")
            
            # Theoretical maximum entropy for comparison
            if file_name == 'random_binary.txt':
                max_entropy = math.log2(2)  # Alphabet size = 2
            elif file_name == 'random_bytes.bin':
                max_entropy = math.log2(256)  # Alphabet size = 256
            else:
                # Estimate alphabet size for text files
                with open(file_name, 'rb') as f:
                    data = f.read()
                unique_bytes = len(set(data))
                max_entropy = math.log2(unique_bytes) if unique_bytes > 0 else 0
            
            # FIX: Check for zero before division
            if max_entropy > 0:
                efficiency = (entropy / max_entropy) * 100
                print(f"  Theoretical max: {max_entropy:.4f} bits | Efficiency: {efficiency:.1f}%")
            else:
                print(f"  Theoretical max: {max_entropy:.4f} bits | Efficiency: N/A")
                
        else:
            print(f"File {file_name} not found!")
    
    print("\n" + "="*50)
    
    # Interactive mode - user can check any file
    print("\nInteractive mode - enter file paths to check their entropy")
    print("(Press Enter to exit)")
    
    while True:
        user_file = input("\nEnter file path: ").strip()
        if not user_file:
            break
        
        if os.path.exists(user_file):
            entropy = calculate_entropy(user_file)
            file_size = os.path.getsize(user_file)
            print(f"Entropy: {entropy:.4f} bits | File size: {file_size} bytes")
        else:
            print("File not found!")

if __name__ == "__main__":
    main()
