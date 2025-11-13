import i18n from "i18next";
import { initReactI18next } from "react-i18next";

const resources = {
  en: {
    translation: {
      "login": "Login",
      "username": "Username",
      "password": "Password",
      "error_invalid_credentials": "Invalid username or password.",
      "user_management": "User Management",
      "roles": "Roles"
    }
  },
  pl: {
    translation: {
      "login": "Logowanie",
      "username": "Nazwa użytkownika",
      "password": "Hasło",
      "error_invalid_credentials": "Nieprawidłowa nazwa użytkownika lub hasło.",
      "user_management": "Zarządzanie użytkownikami",
      "roles": "Role"
    }
  }
};

i18n.use(initReactI18next).init({
  resources,
  lng: "en",
  fallbackLng: "en",
  interpolation: {
    escapeValue: false
  }
});

export default i18n;
