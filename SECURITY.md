# Security Policy

## Supported Versions

We actively support the following versions of StudySage:

| Version | Supported          |
| ------- | ------------------ |
| 1.1.x   | ✅ Yes            |
| 1.0.x   | ⚠️ Limited support |
| < 1.0   | ❌ No             |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in StudySage, please report it responsibly.

### How to Report

1. **Do NOT** create a public GitHub issue for security vulnerabilities
2. Send an email to: [your-email@domain.com] (replace with your actual email)
3. Include "StudySage Security" in the subject line

### What to Include

Please provide as much information as possible:

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact assessment
- Any suggested fixes or mitigations

### Response Timeline

- **Acknowledgment**: Within 24-48 hours
- **Initial Assessment**: Within 1 week
- **Resolution**: Varies based on complexity

### Security Best Practices

When using StudySage:

- **Environment Variables**: Never commit `.env` files or expose tokens
- **Local Only**: StudySage is designed for local use - avoid exposing to public networks
- **Regular Updates**: Keep dependencies updated using `poetry update`
- **Discord Permissions**: Use minimal required permissions for your bot
- **Ollama Security**: Ensure Ollama is not exposed to external networks

## Privacy Considerations

StudySage is designed with privacy in mind:

- **Local Processing**: All AI processing happens locally
- **No External APIs**: No data sent to third-party services
- **Conversation Data**: Stored temporarily in memory only
- **Knowledge Base**: Uses local markdown files only

## Responsible Disclosure

We believe in responsible disclosure. Security researchers who report vulnerabilities in good faith will be acknowledged in our security advisories (with permission).