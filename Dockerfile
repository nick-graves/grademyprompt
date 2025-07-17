FROM public.ecr.aws/lambda/python:3.12

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY handler.py core.py interface.py ./
COPY prompts/ prompts/


CMD ["handler.lambda_handler"]