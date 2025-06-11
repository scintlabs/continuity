# Task-Related Models

This file summarizes the data structures in `base/schema/tasks.py`. They form the payloads passed between workers or stored in the system.

## ToolCall

Represents a call made to a tool. Each call has a unique `call_id`, the `tool_name`, and a dictionary of `arguments` describing what should be executed.

## ToolResult

Holds the outcome of a tool execution. It mirrors `ToolCall` through `call_id` and `tool_name` and stores a `content` payload with the result.

## Task

Defines a unit of work for an agent. A task has an optional `id` and carries `instructions` describing what should be done.

## TaskResult

Captures the output of running a task. It records the originating `task_id` and stores the resulting `content`.

## Process

A collection of tasks that run together. It may have its own `id` and stores a `ProcessResult` when completed.

## ProcessResult

Describes the results of a `Process`. It includes the parent `process_id` and a list of `TaskResult` objects from each task that ran.
