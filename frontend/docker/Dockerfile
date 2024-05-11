# Base image
FROM node:14

# Set working directory
WORKDIR /app

# Add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# Install app dependencies
COPY ./frontend/package.json ./frontend/package-lock.json ./
RUN npm install
RUN npm install react-scripts@latest -g

# Add app
COPY ./frontend ./

# Start app
CMD ["npm", "start"]

# Expose port 3000 to access server
EXPOSE 3000