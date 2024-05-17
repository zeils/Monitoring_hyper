# Используем официальный образ Node.js
FROM node:14

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем package.json и package-lock.json в контейнер
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем все файлы React в контейнер
COPY . .

# Запускаем React-приложение
CMD ["npm", "start"]