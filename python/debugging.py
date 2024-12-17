def calculate_area(radius):
    breakpoint()
    area = 3.14 * radius * radius  # Simple calculation of area
    return area

def process_data(radius):
    print("Starting calculation...")
    area = calculate_area(radius)  # Calls calculate_area function
    print(f"Area of the circle with radius {radius} is {area}")  # Prints the result
    return area

def main():
    radius = 5
    fun_name = "main"
    print("Before calculation")
    
    breakpoint()  # Set a breakpoint here to start debugging
    # Program will pause at the breakpoint. At this point, you're in the interactive debugger.
    # Use the following commands to debug step by step:
    # Press 'n' to go to the next line of code in the current function (next line of main)
    # Press 's' to step into the process_data function (step into that function)
    # Press 'c' to continue execution until the next breakpoint (or program ends)
    # Press 'q' to quit the debugger and stop execution of the program.
    
    fun_name = "main"
    print("first")
    print("After first execution")
    result = process_data(radius)  # Call process_data function
    print("After calculation")  # This will be printed after the function completes

main()
