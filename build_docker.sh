# Build the image
docker build -t text-banner-service .

# Run on port 8000
docker run -d -p 8000:8000 --name banner-gen text-banner-service


