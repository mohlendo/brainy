def brainfuck(source):
    memory = {}  
    brackets = []  
    brackets_counter = 0  
    i = 0  
    pointer = 0
    result = ""

    while i <= len(source) -1:  
        if source[i] == ">":  
            pointer += 1  
        elif source[i] == "<":  
            pointer -= 1  
        elif source[i] == "+":  
            if pointer in memory: memory[pointer] += 1
            else: memory[pointer] = 1
        elif source[i] == "-":  
            memory[pointer] -= 1  
        elif source[i] == ".":  
            result += unichr(memory[pointer])  
        elif source[i] == ",":  
            memory[pointer] = ord(sys.stdin.read(1))  
        elif source[i] == "[":  
            brackets.append(i)  
            brackets_counter += 1  
        elif source[i] == "]":  
            if memory[pointer]:  
                if brackets_counter > 0:  
                     if brackets[brackets_counter-1]:  
                        i = brackets[brackets_counter-1]  
                else:  
                    brackets_counter -= 1  
                    brackets.pop()  
        i += 1
    return result

