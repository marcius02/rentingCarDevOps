# Java Generics Summary

## Intro & Links

- [Oracle Generics](https://docs.oracle.com/javase/tutorial/java/generics/why.html)

> Generics in Java are a **feature** that allows you to define **classes, interfaces, or methods** with <mark>placeholder types</mark> (called type parameters). 
> 
> These placeholders are replaced with specific types when the code is used, enabling reusable, <mark>type-safe code</mark>.

- **Not a class**: But you can create generic classes (e.g., `class Box<T>`).
- **Not a container**: Though often used with collections (e.g., `List<String>`).
- **Not a contract or API**: But generics can define type-safe interfaces (e.g., `interface Pair<K, V>`).
- **Not just an interface**: Generics apply to classes, methods, and interfaces.

In simple terms, generics are like a **template** for writing flexible, type-safe code. For example:

```java
class Box<T> {
    private T item;
    public void set(T item) { this.item = item; }
    public T get() { return item; }
}
```

Here, `T` is a generic type that can be replaced with any type, like `Integer` or `String`, when creating a `Box` (e.g., `Box<Integer>`).

## Why Use Generics?

Generics allow types to be parameters in classes, interfaces, and methods, enabling reusable code with different type inputs. Unlike formal parameters (which use values), type parameters use types.

### Benefits of Generics

1. **Stronger Type Checks at Compile Time**: The Java compiler enforces type safety, catching errors during compilation rather than at runtime, which simplifies debugging.

2. **Elimination of Casts**: Generics remove the need for explicit casting. For example:
   
   - Without generics:
     
     ```java
     List list = new ArrayList();
     list.add("hello");
     String s = (String) list.get(0); // Requires casting
     ```
   
   - With generics:
     
     ```java
     List<String> list = new ArrayList<>();
     list.add("hello");
     String s = list.get(0); // No casting needed
     ```

3. **Generic Algorithms**: Generics enable type-safe, customizable algorithms that work with various collection types, improving readability and maintainability.

## Generic Types

A generic type is a class or interface parameterized over types.

### Non-Generic Box Class

A basic non-generic `Box` class uses `Object` for flexibility but lacks type safety:

```java
public class Box {
    private Object object;
    public void set(Object object) { this.object = object; }
    public Object get() { return object; }
}
```

This allows any type to be stored but risks runtime errors if incorrect types are used.

### Generic Box Class

By introducing a type parameter `T`, the `Box` class becomes type-safe:

```java
/**
 * Generic version of the Box class.
 * @param <T> the type of the value being boxed
 */
public class Box<T> {
    private T t;
    public void set(T t) { this.t = t; }
    public T get() { return t; }
}
```

Here, `T` can represent any non-primitive type (class, interface, array, or another type variable).

## Type Parameter Naming Conventions

Type parameter names are typically single, uppercase letters:

- `E` - Element (used in Java Collections)
- `K` - Key
- `N` - Number
- `T` - Type
- `V` - Value
- `S`, `U`, `V`, etc. - Additional types

This convention distinguishes type parameters from regular variable names.

## Invoking and Instantiating Generic Types

To use a generic class, specify a type argument:

```java
Box<Integer> integerBox; // Declares a Box of Integer
```

Instantiate using the `new` keyword:

```java
Box<Integer> integerBox = new Box<>(); // Diamond notation infers type
```

### The Diamond

In Java SE 7+, the diamond operator (`<>`) allows type inference:

```java
Box<Integer> integerBox = new Box<>(); // No need to repeat <Integer>
```

## Multiple Type Parameters

Generic classes can have multiple type parameters. For example, a `Pair` interface and `OrderedPair` class:

```java
public interface Pair<K, V> {
    public K getKey();
    public V getValue();
}

public class OrderedPair<K, V> implements Pair<K, V> {
    private K key;
    private V value;
    public OrderedPair(K key, V value) {
        this.key = key;
        this.value = value;
    }
    public K getKey() { return key; }
    public V getValue() { return value; }
}
```

Instantiate with specific types:

```java
Pair<String, Integer> p1 = new OrderedPair<>("Even", 8);
Pair<String, String> p2 = new OrderedPair<>("hello", "world");
```

## Parameterized Types

Type parameters can be substituted with parameterized types, e.g.:

```java
OrderedPair<String, Box<Integer>> p = new OrderedPair<>("primes", new Box<>());
```