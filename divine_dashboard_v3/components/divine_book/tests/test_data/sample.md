# Sample Markdown Document

This is a sample markdown document with various code block formats to test the `HighlightRenderer` class.

## Regular Code Block

```
function regularCode() {
  // This is a regular code block with no language specified
  return "regular";
}
```

## Python Code Block

```python
def python_function():
    """This is a Python code block"""
    return "python"
```

## JavaScript Code Block with Info String

```javascript:example.js
function jsFunction() {
    // This has an info string with a filename
    return "javascript with info";
}
```

## Python Code Block with Options

```python {lineNumbers=true}
import os
import sys

def main():
    """This has an info string with options"""
    print("Python with options")

if __name__ == "__main__":
    main()
```

## Ruby Code Block with Additional Info

```ruby filename=example.rb
def ruby_method
  # This has a filename attribute
  puts "Ruby with filename"
end
```

## PHP Code Block with Complex Info

```php showLineNumbers title="Example File" {3-5} :test.php
<?php
function complexInfo() {
    // This has multiple info parameters
    echo "PHP with complex info";
}
?>
```
