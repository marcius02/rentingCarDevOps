# Async

## Intro & Links

> **Asynchronous programming in Java** is a technique that allows tasks to run independently of the main application thread, enabling multiple operations to execute concurrently. 
> 
> This approach is particularly valuable for improving application performance, responsiveness, and scalability, especially in scenarios involving I/O operations, long-running tasks, or high user concurrency.

## Key Concepts

- **Non-blocking Execution:** Async programming lets the main thread continue its work while background tasks are processed, preventing bottlenecks and UI freezes.

- **Concurrency:** Multiple tasks can be managed and executed at the same time, optimizing system resource usage.

- **Thread Management:** Java provides constructs such as `Thread`, `Runnable`, `Callable`, and higher-level abstractions like `ExecutorService` and `ForkJoinPool` for managing concurrent execution.

- **Future and CompletableFuture:**
  
  - `Future<T>` and `ExecutorService` allow you to submit tasks and retrieve results later.
  
  - `CompletableFuture<T>`, introduced in Java 8, enables non-blocking, callback-based async programming with chaining, combining tasks, and robust error handling.

- **Asynchronous I/O:** Java NIO (Non-blocking I/O) supports efficient, scalable network and file operations.

Benefits:

- **Improved Performance:** Tasks run in parallel, reducing idle time and increasing throughput.

- **Enhanced Responsiveness:** Applications remain responsive to user input or other events, even during intensive operations.

- **Scalability:** Async programming allows applications to efficiently handle many simultaneous tasks or users.

- **Better Resource Utilization:** System resources are used more efficiently, as threads are not blocked waiting for slow operations.

Example Usage

```java
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    // Simulate a long-running operation
    return "Hello, CompletableFuture!";
});
future.thenAccept(result -> System.out.println("The Result: " + result));
```

In this example, the main thread is free to continue while the supplied task runs in the background.

## Analogy for 4yo

> Async programming is like a restaurant waiter taking multiple orders and serving dishes as soon as they are ready, rather than waiting for the entire meal to be prepared before serving any customer.

## Implementation

Suppose you have an endpoint `/send-invitations` that triggers sending emails and writing to the DB. 

You want the client to get a  "OK" response, while the actual email sending and DB write happens in the background.

```java
@RestController
public class InvitationController {

    private final InvitationService invitationService;

    public InvitationController(InvitationService invitationService) {
        this.invitationService = invitationService;
    }

    @PostMapping("/send-invitations")
    public ResponseEntity<String> sendInvitations(
            @RequestParam String eventId,
            @RequestBody List<String> invitationIds) {
        // Optionally do some light validation here

        // Trigger async processing
        invitationService.processInvitationsAsync(eventId, invitationIds);

        // Respond immediately
        return ResponseEntity.accepted().body("Invitations are being processed.");
    }
}
```

```java
@Service
public class InvitationService {

    @Async
    public void processInvitationsAsync(String eventId, List<String> invitationIds) {
        // This runs in a background thread pool
        // Do your slow DB write or email sending here
        sendInvitationService.sendInvitations(eventId, invitationIds);
    }
}


@SpringBootApplication
@EnableAsync
public class MyApplication { }
```

## Threads

> When we annotate a method in a Spring-managed `@Service` with `@Async` and call it from another Spring bean, **Spring will execute that method in a separate thread, not the main thread**. 

This means your method runs in the background, freeing up the main thread to handle other requests or operations.

Here’s what happens under the hood:

- **Spring creates a thread pool (by default, or as you configure) and manages it.**

- When your `@Async` method is invoked, **Spring submits it as a task to this thread pool**.

- The method runs on a thread from the pool, not the main application thread.

You can confirm this by logging the thread name inside your async method. For example:

```java
@Async
public void processInvitationsAsync(String eventId, List<String> invitationIds) {
    System.out.println("Running in thread: " + Thread.currentThread().getName());
    // ... your logic ...
}
```

You’ll see output like `Running in thread: SimpleAsyncTaskExecutor-1` or whatever prefix you configured, showing it’s not the main thread.

**Important notes:**

- You must enable async support with `@EnableAsync` in a configuration class for `@Async` to work.

- You can customize the thread pool by defining a `ThreadPoolTaskExecutor` bean if you need more control over concurrency.
