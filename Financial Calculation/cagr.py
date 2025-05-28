def cagr(final, begin, duration):
    """
        final:
        begin:
        duration:
    """
    return (final/begin)**(1/duration) - 1

final = int(input("Enter the final of Return: "))
begin = int(input("Enter the initial amount: "))
duration = int(input("Enter the number of invested years: "))

print(round(cagr(final, begin, duration)*100, 2))