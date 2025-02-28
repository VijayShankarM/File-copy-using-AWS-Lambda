# **S3 to S3 File Copy using AWS Lambda**

## **Overview**
This project automates the process of copying files from one S3 bucket to another using AWS Lambda. Whenever a new file is uploaded to the **source bucket**, a **Lambda function** is triggered to copy the file to the **destination bucket**.

## **Technologies Used**
- **AWS S3** → For storing and transferring files
- **AWS Lambda** → To automate file copying
- **AWS IAM** → To grant permissions for S3 access

---

## **Setup Instructions**

### **Step 1: Create S3 Buckets**
1. Open the **AWS S3 Console**.
2. Click **"Create bucket"**.
3. Enter a unique bucket name (e.g., `source-bucket-yourname`).
4. Leave all other settings as default and click **"Create"**.
5. Repeat the process to create another bucket (e.g., `destination-bucket-yourname`).

---

### **Step 2: Create the Lambda Function**
1. Open the **AWS Lambda Console**.
2. Click **"Create function"** and select **"Author from scratch"**.
3. Enter a function name (e.g., `S3CopyFunction`).
4. Choose **Python 3.x** as the runtime.
5. Click **"Create function"**.

---

### **Step 3: Add an Environment Variable**
1. In the Lambda function, go to **"Configuration"** → **"Environment variables"**.
2. Click **"Edit"**, then **"Add environment variable"**.
3. Enter the following details:
   - **Key**: `DEST_BUCKET`
   - **Value**: `destination-bucket-yourname`
4. Click **"Save"**.

---

### **Step 4: Update IAM Permissions**
1. In the Lambda function, go to **"Configuration"** → **"Permissions"**.
2. Click on the **IAM role name** to open it in the IAM console.
3. Click **"Add permissions"** → **"Attach policies"**.
4. Choose **"Create inline policy"**, and use the following IAM policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::source-bucket-yourname/*",
                "arn:aws:s3:::destination-bucket-yourname/*"
            ]
        }
    ]
}
```
5. Click **"Review policy"**, name it (e.g., `S3CopyPolicy`), and click **"Create policy"**.

---

### **Step 5: Add the Lambda Code**
1. Go to the **"Code"** tab of your Lambda function.
2. Delete any existing code and replace it with the following:

```python
import boto3
import os

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    destination_bucket = os.environ['DEST_BUCKET']
    
    for record in event['Records']:
        source_bucket = record['s3']['bucket']['name']
        file_key = record['s3']['object']['key']
        
        copy_source = {'Bucket': source_bucket, 'Key': file_key}
        s3.copy_object(Bucket=destination_bucket, Key=file_key, CopySource=copy_source)
        
    return {'statusCode': 200, 'body': 'File copied successfully!'}
```
3. Click **"Deploy"**.

---

### **Step 6: Set Up an S3 Trigger**
1. In the Lambda function, go to **"Configuration"** → **"Triggers"**.
2. Click **"Add trigger"**.
3. Select **"S3"** as the trigger source.
4. Choose **source-bucket-yourname** from the dropdown.
5. Set the **Event type** to **"PUT"** (to trigger on file uploads).
6. Click **"Add"**.

---

### **Step 7: Test the Setup**
1. Go to the **AWS S3 Console** and open `source-bucket-yourname`.
2. Upload a test file (e.g., an image or a text file).
3. After a few moments, check `destination-bucket-yourname` to see if the file was copied automatically.

✅ **If the file appears in the destination bucket, the setup is successful!** 🎉




