import builtins

import pandas as pd

# Save the original print function
original_print = builtins.print

# Define a new print function
def print(*args, **kwargs):
    """
    Override the default print function such that dataframes are named.
    """
    for arg in args:
        if isinstance(arg, pd.DataFrame) and hasattr(arg, 'name'):
            original_print(f'{arg.name}:')
            original_print(arg, **kwargs)
        else:
            original_print(arg, **kwargs)


if __name__ == '__main__':
    # Example usage
    df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    df.name = 'MyDataFrame'

    print(df)  # This will print the name of the DataFrame and then the DataFrame itself
    print('Hello, World!')  # This will print normally
