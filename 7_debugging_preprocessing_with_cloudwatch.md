# Debugging Preprocessing With CloudWatch

Assuming your Sagemaker Preprocessing Job has successfully launched, the Logs in your Sagemaker Container will automaticcally be availabe in AWS CloudWatch.

Go to CloudWatch and select the correct region that you used to run your Sagemaker jobs. Then click **Logs->Log Groups**, select Log Group **Streams for /aws/sagemaker/ProcessingJobs** to display all the Preprocessing Jobs. Select the one you are interested to display the log information.
