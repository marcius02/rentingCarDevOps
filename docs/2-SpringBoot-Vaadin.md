# Spring Boot Vaadin Guide

## Introduction

> <mark>Vaadin is a Java framework</mark> for building modern, full-stack web applications with a focus on developer productivity and rich user interfaces. 
> 
> When integrated with Spring Boot, Vaadin enables rapid development of business applications using either **Vaadin Flow (server-side Java)** or **Hilla (React-based frontend with Spring Boot backend).**

**Useful Links:**

- [Vaadin Official Documentation](https://vaadin.com/docs)
- [Spring Boot with Vaadin Guide](https://vaadin.com/docs/latest/guide/spring)
- [Start Vaadin](https://start.vaadin.com)

## Spring Boot Vaadin

Spring Boot simplifies Vaadin application development by providing **auto-configuration,** dependency management, and a **production-ready web server**. 

Vaadin integrates seamlessly with Spring Boot, leveraging Spring’s features like dependency injection, security, and data access.

- **Key Benefits**:
  - Build full-stack applications with Java or combine Java with React.
  - Use Spring Data for database integration and Spring Security for authentication.
  - Automatic configuration of Vaadin with Spring Boot via `vaadin-spring-boot-starter`.
- **Setup**:
  - Create a project using [start.vaadin.com](https://start.vaadin.com) or Spring Initializr.
  - Add the Vaadin dependency in `pom.xml`:
    
    ```xml
    <dependency>
        <groupId>com.vaadin</groupId>
        <artifactId>vaadin-spring-boot-starter</artifactId>
    </dependency>
    ```
  - Run the application with `mvn spring-boot:run` or from your IDE.

## Flow and Hilla

Vaadin offers two frameworks for building web applications:

- **Vaadin Flow**:
  
  - A server-side Java framework for creating web UIs without writing JavaScript or HTML.
  
  - Ideal for data-rich business applications.
  
  - Components are defined in Java, with an event-driven model for user interactions.
  
  - Example:
    
    ```java
    import com.vaadin.flow.component.button.Button;
    import com.vaadin.flow.component.notification.Notification;
    import com.vaadin.flow.component.orderedlayout.VerticalLayout;
    import com.vaadin.flow.router.Route;
    
    @Route("")
    public class MainView extends VerticalLayout {
        public MainView() {
            Button button = new Button("Click me");
            button.addClickListener(e -> Notification.show("Hello, Vaadin!"));
            add(button);
        }
    }
    ```
  
  - Best for: Developers preferring a Java-only stack.

- **Hilla**:
  
  - A full-stack framework combining a Spring Boot backend with a React frontend.
  
  - Uses TypeScript for frontend development, with auto-generated APIs for backend communication.
  
  - Example:
    
    ```typescript
    // Frontend/views/HelloView.tsx
    import { useSignal } from '@vaadin/hilla-react-signals';
    import { Button } from '@vaadin/react-components/Button.js';
    
    export default function HelloView() {
        const message = useSignal('Hello, Hilla!');
        return (
            <div>
                <Button onClick={() => (message.value = 'Clicked!')}>{message.value}</Button>
            </div>
        );
    }
    ```
  
  - Best for: Applications needing a modern React frontend with Spring Boot backend.

- **Hybrid Applications**:
  
  - Vaadin 24.4+ unifies Flow and Hilla, allowing React-based routes in Flow apps or Flow components in Hilla apps.[](https://vaadin.com/docs/latest/upgrading)
  - Add Hilla to a Flow project by including a frontend view (e.g., `counter.tsx`) in `src/main/frontend/views`.

## Vaadin Playground

The Vaadin Playground is an online tool for experimenting with Vaadin Flow and Hilla without local setup.

- **URL**: [https://start.vaadin.com/app/p](https://start.vaadin.com/app/p)

- **Features**:
  
  - Write and test Vaadin Flow or Hilla code in a browser-based IDE.
  - Instant previews of UI components and layouts.
  - Shareable code snippets for collaboration or learning.

- **Use Cases**:
  
  - Prototyping UI designs.
  - Learning Vaadin components and APIs.
  - Testing small code changes before integrating into a project.

- **Example**:
  
  - Open the playground, select Flow or Hilla, and try a simple component like:
    
    ```java
    // Flow example in Playground
    import com.vaadin.flow.component.button.Button;
    import com.vaadin.flow.component.html.Span;
    import com.vaadin.flow.component.orderedlayout.VerticalLayout;
    import com.vaadin.flow.router.Route;
    
    @Route("")
    public class PlaygroundView extends VerticalLayout {
        public PlaygroundView() {
            add(new Span("Welcome to Vaadin Playground!"));
            add(new Button("Test", e -> add(new Span("Button clicked!"))));
        }
    }
    ```

## Starter Project

Vaadin provides a customizable starter project template for Spring Boot applications, available at [https://start.vaadin.com/app](https://start.vaadin.com/app). This tool generates a "walking skeleton"—a minimal, functional application that you can extend.

### Dependencies

- **Java 21 TLS**:
  - Vaadin 24 requires Java 17 or later, with Java 21 recommended for long-term support (TLS).
  - Configure `pom.xml` for Java 21:
    
    ```xml
    <properties>
        <java.version>21</java.version>
    </properties>
    ```
- **Vaadin 24.7**:
  - The latest stable version as of April 2025, with support until June 2026.[](https://vaadin.com/roadmap)
  - Add Vaadin BOM and dependencies:
    
    ```xml
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>com.vaadin</groupId>
                <artifactId>vaadin-bom</artifactId>
                <version>24.7.2</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>com.vaadin</groupId>
            <artifactId>vaadin-spring-boot-starter</artifactId>
        </dependency>
    </dependencies>
    ```
  - Optionally exclude Hilla if only using Flow:
    
    ```xml
    <dependency>
        <groupId>com.vaadin</groupId>
        <artifactId>vaadin</artifactId>
        <exclusions>
            <exclusion>
                <groupId>com.vaadin</groupId>
                <artifactId>hilla</artifactId>
            </exclusion>
        </exclusions>
    </dependency>
    ```
- **Additional Dependencies**:
  - Spring Boot Starter (e.g., `spring-boot-starter-web`).
  - Optional: Spring Data JPA, Spring Security, or database drivers (e.g., PostgreSQL, MySQL).

### Include Walking Skeleton

- The starter project from [start.vaadin.com](https://start.vaadin.com/app) includes a walking skeleton—a minimal app with:
  
  - A main view with basic Vaadin components (e.g., `Button`, `TextField`).
  - Spring Boot configuration with auto-wired services.
  - Live reload via Spring Boot Developer Tools for rapid development.[](https://github.com/vaadin/skeleton-starter-flow-spring)

- **Structure**:
  
  - `src/main/java`: Java classes for Flow views or Hilla services.
  - `src/main/frontend`: TypeScript/React files for Hilla views.
  - `pom.xml`: Maven configuration with Vaadin and Spring Boot dependencies.

- **Example Walking Skeleton**:
  
  - Generated Flow project includes:
    
    ```java
    package com.example.application;
    
    import com.vaadin.flow.component.orderedlayout.VerticalLayout;
    import com.vaadin.flow.router.Route;
    import com.vaadin.flow.component.button.Button;
    
    @Route("")
    public class MainView extends VerticalLayout {
        public MainView() {
            add(new Button("Hello, Vaadin!", e -> add(new com.vaadin.flow.component.html.Span("Clicked!"))));
        }
    }
    ```
  
  - Generated Hilla project includes a React view and Spring service:
    
    ```typescript
    // src/main/frontend/views/hello/HelloView.tsx
    import { Button } from '@vaadin/react-components/Button.js';
    
    export default function HelloView() {
        return <Button onClick={() => alert('Hello, Hilla!')}>Click me</Button>;
    }
    ```

### Running the Starter Project

- **IDE**: Import the project as a Maven project and run the `Application` class.
- **Command Line**: Use `mvn spring-boot:run` and open `http://localhost:8080`.
- **Production Build**: Run `mvn clean package -Pproduction` for a production-ready WAR file.[](https://github.com/vaadin/skeleton-starter-flow-spring)
- **Live Reload**: Enabled by default with Spring Boot Developer Tools; browser refresh may be needed.[](https://github.com/vaadin/skeleton-starter-flow-spring)

## Additional Resources

- **Tutorials**: [Vaadin Tutorials](https://vaadin.com/tutorials)
- **Components**: [Vaadin Components](https://vaadin.com/components)
- **Examples**: [Vaadin Examples and Demos](https://vaadin.com/examples-and-demos)
- **Community**: Ask questions on [Stack Overflow](https://stackoverflow.com/questions/tagged/vaadin) or join the [Vaadin Discord](https://discord.gg/vaadin).
- **GitHub**: [Vaadin Skeleton Starter](https://github.com/vaadin/skeleton-starter-flow-spring)[](https://github.com/vaadin/skeleton-starter-flow-spring)