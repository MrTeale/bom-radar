# Migration from Serverless Framework to AWS SAM

This document outlines the migration from Serverless Framework to AWS SAM for the BOM Radar project.

## What Changed

### Files Added
- `template.yaml` - AWS SAM template (replaces `serverless.yml`)
- `samconfig.toml` - SAM deployment configuration
- `.github/workflows/deploy.yml` - GitHub Actions CI/CD workflow
- `MIGRATION.md` - This migration guide

### Files You Can Remove (After Testing)
- `serverless.yml` - Old Serverless Framework config
- `package.json` - Only needed for Serverless Framework plugins
- `package-lock.json` - Only needed for Serverless Framework plugins
- `node_modules/` - No longer needed

## Prerequisites

1. **AWS SAM CLI** installed locally (for local testing)
   ```bash
   # macOS
   brew install aws-sam-cli

   # Linux
   pip install aws-sam-cli

   # Windows
   # Download from: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html
   ```

2. **AWS Credentials** configured
   ```bash
   aws configure
   ```

## GitHub Actions Setup

### Option 1: OIDC (Recommended - More Secure)

1. Create an IAM OIDC provider for GitHub in AWS Console
2. Create an IAM role with trust policy for GitHub Actions
3. Add the role ARN as a GitHub repository secret:
   - Secret name: `AWS_ROLE_ARN`
   - Value: `arn:aws:iam::YOUR_ACCOUNT_ID:role/GitHubActionsRole`

### Option 2: Access Keys (Simpler, Less Secure)

1. Create an IAM user with programmatic access
2. Attach policies: `AWSLambdaFullAccess`, `IAMFullAccess`, `AmazonAPIGatewayAdministrator`, `CloudFormationFullAccess`
3. Add credentials as GitHub repository secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
4. Update `.github/workflows/deploy.yml` to use access keys (see commented section)

## Deployment

### Automatic Deployment (GitHub Actions)
Pushes to the `main` branch will automatically trigger deployment.

### Manual Deployment

```bash
# Build the application
sam build

# Deploy to AWS (will reuse existing stack)
sam deploy
```

### First-Time Deployment

If this is a fresh deployment (not reusing existing resources):

```bash
sam build
sam deploy --guided
```

This will prompt you for:
- Stack name (use: `bom-radar`)
- AWS Region (use: `us-east-1` or your current region)
- Confirm changes before deploy
- Allow SAM CLI IAM role creation
- Disable rollback
- Save arguments to configuration file

## Custom Domain Setup

The current SAM template includes the API Gateway configuration but does **not** automatically set up the custom domain (`radar.lachlanteale.com`).

### To Keep Your Custom Domain:

1. **If you're using Serverless Framework's domain manager**, keep it running until migration is complete
2. After deploying with SAM, you'll need to:
   - Update the API Gateway custom domain mapping in AWS Console
   - Point it to the new API Gateway created by SAM
   - OR use AWS Certificate Manager and API Gateway v2 custom domains

### Alternative: Manual Custom Domain Setup

```bash
# Get your API Gateway ID
aws cloudformation describe-stacks \
  --stack-name bom-radar \
  --query 'Stacks[0].Outputs[?OutputKey==`BomRadarApi`].OutputValue' \
  --output text

# Update your custom domain mapping in API Gateway console
# to point to the new API Gateway ID
```

## Verifying the Migration

1. Deploy using SAM:
   ```bash
   sam build && sam deploy
   ```

2. Test the endpoint:
   ```bash
   # Get the API endpoint
   aws cloudformation describe-stacks \
     --stack-name bom-radar \
     --query 'Stacks[0].Outputs[?OutputKey==`BomRadarApi`].OutputValue' \
     --output text

   # Test it
   curl -o test-radar.gif "YOUR_API_ENDPOINT"
   ```

3. Verify the GIF image is generated correctly

## Resource Reuse

The SAM template is designed to **reuse** your existing AWS resources:
- **IAM Role**: Uses the same name `BOMIAMRole`
- **Lambda Function**: Uses the same naming pattern `bom-radar-prod-main`
- **API Gateway**: Creates a new API with the same stage name `prod`

CloudFormation will update resources where possible instead of recreating them.

## Rollback Plan

If something goes wrong, you can rollback:

```bash
# Rollback via CloudFormation
aws cloudformation cancel-update-stack --stack-name bom-radar

# Or delete and redeploy with Serverless Framework
aws cloudformation delete-stack --stack-name bom-radar
serverless deploy
```

## Key Differences

| Feature | Serverless Framework | AWS SAM |
|---------|---------------------|---------|
| Config File | `serverless.yml` | `template.yaml` |
| CLI Command | `serverless deploy` | `sam deploy` |
| Build Step | Automatic | `sam build` required |
| Local Testing | `serverless invoke local` | `sam local invoke` |
| Plugins | Required for Python deps | Built-in support |
| Custom Domains | Plugin-based | CloudFormation native |
| Speed | Slower | Faster |

## Troubleshooting

### Issue: Stack already exists
This is expected! SAM will update the existing stack, not recreate it.

### Issue: IAM role name conflict
If you get an IAM role name conflict, the stack will update the existing role rather than create a new one.

### Issue: Binary response not working
Ensure the API Gateway binary media types are configured correctly in `template.yaml` (already done).

### Issue: Custom domain not working
You may need to manually update the custom domain mapping in API Gateway console after migration.

## Next Steps

After successful migration:

1. Remove old Serverless Framework files:
   ```bash
   rm serverless.yml package.json package-lock.json
   rm -rf node_modules/
   ```

2. Update your documentation to reflect SAM usage

3. Configure GitHub Actions secrets for automated deployments

4. Test the GitHub Actions workflow by pushing to `main`

## Support

- AWS SAM Documentation: https://docs.aws.amazon.com/serverless-application-model/
- GitHub Actions for AWS: https://github.com/aws-actions/configure-aws-credentials
