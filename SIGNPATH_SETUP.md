# SignPath.io Setup for WTOP

## Overview
SignPath.io provides free code signing for open source projects. This guide walks through setting up automated code signing for WTOP releases.

## Prerequisites
- GitHub repository (✓ Already have: https://github.com/Zazarothh/wtop)
- Open source license (✓ Already have: MIT License)
- Active development (✓ Already demonstrated)

## Step 1: Apply for SignPath Open Source Program

1. Go to https://signpath.io/pricing (scroll to "Open Source")
2. Click "Apply for free subscription"
3. Fill out the application:
   - **Project Name**: WTOP - Terminal Weather Dashboard
   - **Repository URL**: https://github.com/Zazarothh/wtop
   - **License**: MIT
   - **Description**: A terminal-based weather dashboard that displays real-time weather information with ASCII art
   - **Project Website**: https://github.com/Zazarothh/wtop
   - **Contact Email**: [Your email]

## Step 2: Wait for Approval
- Usually takes 2-5 business days
- You'll receive an email with your organization details
- You'll get access to the SignPath dashboard

## Step 3: Configure SignPath Project

Once approved, in your SignPath dashboard:

1. Create a new project called "WTOP"
2. Add a signing configuration:
   - **Name**: "Release Signing"
   - **Certificate**: Use SignPath's provided certificate
   - **Signing Method**: Authenticode

## Step 4: Get Your Credentials

From SignPath dashboard:
1. Go to "CI/CD Integration"
2. Note down:
   - Organization ID
   - Project Slug (usually "wtop")
   - Signing Policy Slug (usually "release-signing")
   - API Token (create one if needed)

## Step 5: Add GitHub Secrets

In your GitHub repository (https://github.com/Zazarothh/wtop):
1. Go to Settings → Secrets and variables → Actions
2. Add these secrets:
   - `SIGNPATH_API_TOKEN`: Your SignPath API token
   - `SIGNPATH_ORGANIZATION_ID`: Your org ID
   - `SIGNPATH_PROJECT_SLUG`: wtop
   - `SIGNPATH_SIGNING_POLICY_SLUG`: release-signing

## Step 6: GitHub Actions Workflow

The workflow file (`.github/workflows/build-and-sign.yml`) is already created in this repository.
It will automatically:
1. Build the executable with PyInstaller
2. Upload it to SignPath for signing
3. Download the signed executable
4. Create a GitHub release with the signed exe

## Step 7: Test the Workflow

1. Push a new tag to trigger a release:
```bash
git tag v1.0.2
git push origin v1.0.2
```

2. Check Actions tab in GitHub to monitor the workflow
3. Once complete, the signed exe will be in the release

## Manual Signing (Alternative)

If you prefer to sign manually:

1. Build your exe locally:
```bash
pyinstaller --onefile --name wtop wtop.py
```

2. Upload to SignPath dashboard manually
3. Download the signed exe
4. Upload to GitHub release

## Verification

After signing, users will see:
- **Publisher**: "SignPath Foundation" or your name (if using personal certificate)
- **No SmartScreen warnings** for EV certificates
- **Reduced warnings** for standard certificates after building reputation

## Troubleshooting

### Application Rejected
- Ensure your project is actively maintained
- Must have clear open source license
- Repository should have meaningful content

### Signing Fails
- Check file size limits (usually 100MB)
- Ensure exe is not already signed
- Verify API credentials are correct

### Still Getting Warnings
- Standard certificates need reputation building
- First ~100-500 downloads may still show warnings
- EV certificates provide instant trust

## Resources
- SignPath Docs: https://docs.signpath.io/
- SignPath Open Source: https://signpath.io/open-source
- GitHub Actions Integration: https://docs.signpath.io/build-system-integration/github-actions

## Support
- SignPath Support: support@signpath.io
- GitHub Issues: https://github.com/Zazarothh/wtop/issues