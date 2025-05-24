# Contributing to StudySage

Thank you for your interest in contributing to StudySage! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Issues

1. Check existing issues to avoid duplicates
2. Use the issue template when creating new issues
3. Provide clear reproduction steps for bugs
4. Include system information (OS, Python version, etc.)

### Submitting Changes

1. **Fork the repository**
2. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following the coding standards below
4. **Test thoroughly** - ensure bot works with your changes
5. **Commit with descriptive messages** using conventional commits:
   ```bash
   git commit -m "feat: add new knowledge domain for computer vision"
   git commit -m "fix: resolve async timeout in generation module"
   git commit -m "docs: improve installation instructions"
   ```
6. **Submit a pull request** with a clear description

## Development Setup

1. Clone your fork and install dependencies:
   ```bash
   git clone https://github.com/YOUR_USERNAME/StudySage.git
   cd StudySage
   poetry install
   ```

2. Set up your development environment:
   ```bash
   cp .env.example .env
   # Configure your .env file
   ```

3. Ensure Ollama is running:
   ```bash
   ollama pull mistral
   ollama serve
   ```

## Coding Standards

- **Python Style**: Follow PEP 8
- **Documentation**: Add docstrings for all functions and classes
- **Type Hints**: Use type annotations where appropriate
- **Error Handling**: Include proper error handling and logging
- **Testing**: Test your changes thoroughly before submitting

## Areas for Contribution

### High Priority
- **Knowledge Base Expansion**: Add new AI/ML topic documents
- **Performance Optimization**: Improve vector search or LLM response times
- **Error Handling**: Enhance robustness and user experience

### Medium Priority
- **Evaluation Metrics**: Add response quality measurement tools
- **Configuration**: Improve setup and configuration flexibility
- **Documentation**: Enhance tutorials and examples

### Advanced
- **Multi-language Support**: Internationalization features
- **Advanced RAG**: Implement more sophisticated retrieval strategies
- **Monitoring**: Add performance monitoring and analytics

## Pull Request Guidelines

- **Title**: Use descriptive titles that explain the change
- **Description**: Include motivation, changes made, and testing notes
- **Scope**: Keep changes focused - one feature/fix per PR
- **Testing**: Verify your changes work with existing functionality
- **Documentation**: Update README or docs if needed

## Questions?

Feel free to open an issue for questions about contributing or reach out to the maintainers.

Thank you for contributing to StudySage!