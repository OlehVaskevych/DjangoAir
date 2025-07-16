<template>
  <div class="auth-modals">
    <!-- Кнопки для відкриття модальних вікон на головній сторінці -->
    <div class="auth-buttons" v-if="currentSection === 'intro'">
      <button @click="showLoginModal" class="btn-auth btn-login">
        <span>Sign in</span>
      </button>
      <button @click="showRegisterModal" class="btn-auth btn-register">
        <span>Sign up</span>
      </button>
    </div>

    <!-- Модальне вікно входу -->
    <div class="modal-overlay" v-if="isLoginModalVisible" @click="closeModals">
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <h2 class="modal-title">Sign in</h2>
          <button class="modal-close" @click="closeModals">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleLogin">
            <!-- Загальна помилка для форми логіну -->
            <transition name="fade-slide-down">
              <div v-if="loginErrors.general" class="form-error general-error">
                {{ loginErrors.general }}
              </div>
            </transition>

            <div class="form-group">
              <label for="login-email">Email</label>
              <div class="input-wrapper" :class="{ 'has-error': loginErrors.email }">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="input-icon">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                  <polyline points="22,6 12,13 2,6"></polyline>
                </svg>
                <input
                  type="email"
                  id="login-email"
                  v-model="loginForm.email"
                  required
                  placeholder="your.email@example.com"
                  class="form-input"
                  :class="{ 'input-error': loginErrors.email }"
                >
              </div>
              <transition name="fade-slide-up">
                <div v-if="loginErrors.email" class="form-error">
                  {{ loginErrors.email }}
                </div>
              </transition>
            </div>

            <div class="form-group">
              <label for="login-password">Password</label>
              <div class="input-wrapper" :class="{ 'has-error': loginErrors.password }">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="input-icon">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
                <input
                  :type="showLoginPassword ? 'text' : 'password'"
                  id="login-password"
                  v-model="loginForm.password"
                  required
                  placeholder="••••••••"
                  class="form-input"
                  :class="{ 'input-error': loginErrors.password }"
                >
                <button
                  type="button"
                  class="password-toggle"
                  @click="showLoginPassword = !showLoginPassword"
                >
                  <svg v-if="!showLoginPassword" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                    <line x1="1" y1="1" x2="23" y2="23"></line>
                  </svg>
                </button>
              </div>
              <transition name="fade-slide-up">
                <div v-if="loginErrors.password" class="form-error">
                  {{ loginErrors.password }}
                </div>
              </transition>
            </div>

            <div class="form-options">
              <label class="checkbox-container">
                <input type="checkbox" v-model="loginForm.rememberMe">
                <span class="checkmark"></span>
                <span>Remember me</span>
              </label>
              <a href="#" class="forgot-password">Forgot password?</a>
            </div>

            <button type="submit" class="btn-submit" :disabled="isSubmitting">
              <span v-if="isSubmitting">
                <svg class="spinner" viewBox="0 0 50 50">
                  <circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle>
                </svg>
                Loading...
              </span>
              <span v-else>Sign in</span>
              <div class="btn-particles"></div>
            </button>
          </form>
          <div class="social-login">
            <p>Or sign in with</p>
            <div class="social-buttons">
              <button @click="redirectToOAuth('google')" type="button" class="social-btn google">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12.545,10.239v3.821h5.445c-0.712,2.315-2.647,3.972-5.445,3.972c-3.332,0-6.033-2.701-6.033-6.032s2.701-6.032,6.033-6.032c1.498,0,2.866,0.549,3.921,1.453l2.814-2.814C17.503,2.988,15.139,2,12.545,2C7.021,2,2.543,6.477,2.543,12s4.478,10,10.002,10c8.396,0,10.249-7.85,9.426-11.748L12.545,10.239z"/>
                </svg>
                <span>Google</span>
              </button>
            </div>
          </div>
          <div class="modal-footer">
            <p>Do not have account yet? <a href="#" @click.prevent="switchToRegister">Register</a></p>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальне вікно реєстрації -->
    <div class="modal-overlay" v-if="isRegisterModalVisible" @click="closeModals">
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <h2 class="modal-title">Account Creating</h2>
          <button class="modal-close" @click="closeModals">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleRegister">
            <!-- Загальна помилка для форми реєстрації -->
            <transition name="fade-slide-down">
              <div v-if="registerErrors.general" class="form-error general-error">
                {{ registerErrors.general }}
              </div>
            </transition>

            <div class="form-row">
              <div class="form-group">
                <label for="register-firstname">First Name</label>
                <div class="input-wrapper" :class="{ 'has-error': registerErrors.firstName }">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="input-icon">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                  </svg>
                  <input
                    type="text"
                    id="register-firstname"
                    v-model="registerForm.firstName"
                    required
                    placeholder="Ім'я"
                    class="form-input"
                    :class="{ 'input-error': registerErrors.firstName }"
                  >
                </div>
                <transition name="fade-slide-up">
                <div v-if="registerErrors.firstName" class="form-error">
                  <ul>
                    <li v-for="(error, idx) in registerErrors.firstName" :key="idx">
                      {{ error }}
                    </li>
                  </ul>
                </div>
              </transition>
              </div>
              <div class="form-group">
                <label for="register-lastname">Last Name</label>
                <div class="input-wrapper" :class="{ 'has-error': registerErrors.lastName }">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="input-icon">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                  </svg>
                  <input
                    type="text"
                    id="register-lastname"
                    v-model="registerForm.lastName"
                    required
                    placeholder="Прізвище"
                    class="form-input"
                    :class="{ 'input-error': registerErrors.lastName }"
                  >
                </div>
                <transition name="fade-slide-up">
                <div v-if="registerErrors.lastName" class="form-error">
                  <ul>
                    <li v-for="(error, idx) in registerErrors.lastName" :key="idx">
                      {{ error }}
                    </li>
                  </ul>
                </div>
              </transition>
              </div>
            </div>

            <div class="form-group">
              <label for="register-email">Email</label>
              <div class="input-wrapper" :class="{ 'has-error': registerErrors.email }">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="input-icon">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                  <polyline points="22,6 12,13 2,6"></polyline>
                </svg>
                <input
                  type="email"
                  id="register-email"
                  v-model="registerForm.email"
                  required
                  placeholder="your.email@example.com"
                  class="form-input"
                  :class="{ 'input-error': registerErrors.email }"
                >
              </div>
              <transition name="fade-slide-up">
                <div v-if="registerErrors.email" class="form-error">
                  <ul>
                    <li v-for="(error, idx) in registerErrors.email" :key="idx">
                      {{ error }}
                    </li>
                  </ul>
                </div>
              </transition>
            </div>

            <div class="form-group">
              <label for="register-password">Password</label>
              <div class="input-wrapper" :class="{ 'has-error': registerErrors.password }">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="input-icon">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
                <input
                  :type="showRegisterPassword ? 'text' : 'password'"
                  id="register-password"
                  v-model="registerForm.password"
                  required
                  placeholder="••••••••"
                  class="form-input"
                  :class="{ 'input-error': registerErrors.password }"
                >
                <button
                  type="button"
                  class="password-toggle"
                  @click="showRegisterPassword = !showRegisterPassword"
                >
                  <svg v-if="!showRegisterPassword" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                    <line x1="1" y1="1" x2="23" y2="23"></line>
                  </svg>
                </button>
              </div>
              <transition name="fade-slide-up">
                <div v-if="registerErrors.password" class="form-error">
                  <ul>
                    <li v-for="(error, idx) in registerErrors.password" :key="idx">
                      {{ error }}
                    </li>
                  </ul>
                </div>
              </transition>
              <div class="password-strength" v-if="registerForm.password">
                <div class="strength-meter">
                  <div
                    class="strength-bar"
                    :style="{ width: passwordStrength + '%', backgroundColor: passwordStrengthColor }"
                  ></div>
                </div>
                <span class="strength-text" :style="{ color: passwordStrengthColor }">
                  {{ passwordStrengthText }}
                </span>
              </div>
            </div>

            <div class="form-group">
              <label for="register-confirm-password">Password Confirmation</label>
              <div class="input-wrapper" :class="{ 'has-error': registerErrors.confirmPassword || passwordsDoNotMatch }">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="input-icon">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
                <input
                  :type="showRegisterConfirmPassword ? 'text' : 'password'"
                  id="register-confirm-password"
                  v-model="registerForm.confirmPassword"
                  required
                  placeholder="••••••••"
                  class="form-input"
                  :class="{ 'input-error': registerErrors.confirmPassword || passwordsDoNotMatch }"
                >
                <button
                  type="button"
                  class="password-toggle"
                  @click="showRegisterConfirmPassword = !showRegisterConfirmPassword"
                >
                  <svg v-if="!showRegisterConfirmPassword" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                    <line x1="1" y1="1" x2="23" y2="23"></line>
                  </svg>
                </button>
              </div>
              <transition name="fade-slide-up">
                <div v-if="registerErrors.confirmPassword || passwordsDoNotMatch" class="form-error">
                  {{ registerErrors.confirmPassword || 'Паролі не співпадають' }}
                </div>
              </transition>
            </div>

            <div class="form-options">
              <label class="checkbox-container">
                <input type="checkbox" v-model="registerForm.agreeTerms" required>
                <span class="checkmark"></span>
                <span>I agree to the <a href="#">Terms of Use</a> and <a href="#">Privacy Policy</a></span>
              </label>
              <transition name="fade-slide-up">
                <div v-if="registerErrors.agreeTerms" class="form-error">
                  {{ registerErrors.agreeTerms }}
                </div>
              </transition>
            </div>

            <button type="submit" class="btn-submit" :disabled="isSubmitting || !canRegister">
              <span v-if="isSubmitting">
                <svg class="spinner" viewBox="0 0 50 50">
                  <circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle>
                </svg>
                Loading...
              </span>
              <span v-else>Sign Up</span>
              <div class="btn-particles"></div>
            </button>
          </form>
          <div class="social-login">
            <p>Or register with</p>
            <div class="social-buttons">
              <button @click="redirectToOAuth('google')" type="button" class="social-btn google">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12.545,10.239v3.821h5.445c-0.712,2.315-2.647,3.972-5.445,3.972c-3.332,0-6.033-2.701-6.033-6.032s2.701-6.032,6.033-6.032c1.498,0,2.866,0.549,3.921,1.453l2.814-2.814C17.503,2.988,15.139,2,12.545,2C7.021,2,2.543,6.477,2.543,12s4.478,10,10.002,10c8.396,0,10.249-7.85,9.426-11.748L12.545,10.239z"/>
                </svg>
                <span>Google</span>
              </button>
            </div>
          </div>
          <div class="modal-footer">
            <p>Already have an account? <a href="#" @click.prevent="switchToLogin">Log in</a></p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { emitter, EventTypes } from '@/scripts/eventBus';

export default {
  props: {
    currentSection: {
      type: String,
      default: 'intro'
    }
  },
  data() {
    return {
      isLoginModalVisible: false,
      isRegisterModalVisible: false,
      showLoginPassword: false,
      showRegisterPassword: false,
      showRegisterConfirmPassword: false,
      loginForm: {
        email: '',
        password: '',
        rememberMe: false
      },
      registerForm: {
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        confirmPassword: '',
        agreeTerms: false
      },
      // Додаємо стани для зберігання помилок
      loginErrors: {
        general: '',
        email: '',
        password: ''
      },
      registerErrors: {
        general: '',
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        confirmPassword: '',
        agreeTerms: ''
      },
      isSubmitting: false
    }
  },
  computed: {
    passwordsDoNotMatch() {
      return this.registerForm.password &&
             this.registerForm.confirmPassword &&
             this.registerForm.password !== this.registerForm.confirmPassword;
    },
    passwordStrength() {
      if (!this.registerForm.password) return 0;

      let strength = 0;
      const password = this.registerForm.password;

      // Довжина паролю
      if (password.length >= 8) strength += 25;

      // Наявність цифр
      if (/\d/.test(password)) strength += 25;

      // Наявність малих літер
      if (/[a-z]/.test(password)) strength += 25;

      // Наявність великих літер
      if (/[A-Z]/.test(password)) strength += 25;

      return strength;
    },
    passwordStrengthText() {
      if (this.passwordStrength <= 25) return 'Слабкий';
      if (this.passwordStrength <= 50) return 'Середній';
      if (this.passwordStrength <= 75) return 'Хороший';
      return 'Сильний';
    },
    passwordStrengthColor() {
      if (this.passwordStrength <= 25) return '#ff4757';
      if (this.passwordStrength <= 50) return '#ffa502';
      if (this.passwordStrength <= 75) return '#2ed573';
      return '#7bed9f';
    },
    canRegister() {
      return this.registerForm.agreeTerms &&
             !this.passwordsDoNotMatch &&
             this.registerForm.password &&
             this.registerForm.confirmPassword;
    }
  },
  methods: {
    // Метод для очищення помилок логіну
    clearLoginErrors() {
      this.loginErrors = {
        general: '',
        email: '',
        password: ''
      };
    },

    // Метод для очищення помилок реєстрації
    clearRegisterErrors() {
      this.registerErrors = {
        general: '',
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        confirmPassword: '',
        agreeTerms: ''
      };
    },

    showLoginModal() {
      this.clearLoginErrors();
      this.isLoginModalVisible = true;
      this.isRegisterModalVisible = false;
    },

    showRegisterModal() {
      this.clearRegisterErrors();
      this.isRegisterModalVisible = true;
      this.isLoginModalVisible = false;
    },

    closeModals() {
      this.isLoginModalVisible = false;
      this.isRegisterModalVisible = false;
      this.clearLoginErrors();
      this.clearRegisterErrors();
    },

    switchToRegister() {
      this.clearLoginErrors();
      this.clearRegisterErrors();
      this.isLoginModalVisible = false;
      this.isRegisterModalVisible = true;
    },

    switchToLogin() {
      this.clearLoginErrors();
      this.clearRegisterErrors();
      this.isRegisterModalVisible = false;
      this.isLoginModalVisible = true;
    },

    async handleLogin(event) {
      event.preventDefault();

      // Скидаємо попередні помилки
      this.clearLoginErrors();

      // Валідація на стороні клієнта
      if (!this.loginForm.email) {
        this.loginErrors.email = 'Email обов\'язковий';
        return;
      }

      if (!this.loginForm.password) {
        this.loginErrors.password = 'Пароль обов\'язковий';
        return;
      }

      // Встановлюємо стан завантаження
      this.isSubmitting = true;

      const loginData = {
        email: this.loginForm.email,
        password: this.loginForm.password,
        rememberMe: this.loginForm.rememberMe,
      }

      try {
        const response = await fetch('/auth/login/', {
          method: 'POST',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          body: new URLSearchParams(loginData),
          credentials: "include",
        });

        const data = await response.json();

        if (data.success) {
          // Оновлюємо дані користувача
          if (data.user) {
            const userData = {
              name: data.user.name || '',
              email: data.user.email || '',
              id: data.user.id || null
            };

            // Зберігаємо дані в localStorage
            localStorage.setItem('userData', JSON.stringify(userData));
            localStorage.setItem('isAuthenticated', 'true');

            // Використовуємо emitter замість this.$emit
            emitter.emit(EventTypes.AUTH.LOGIN_SUCCESS, userData);

            // Закриваємо модальне вікно
            this.closeModals();
          }
        } else {
          // Обробка помилок від сервера
          if (data.errors) {
            // Якщо сервер повертає об'єкт з помилками для конкретних полів
            if (data.errors.email) {
              this.loginErrors.email = data.errors.email;
            }
            if (data.errors.password) {
              this.loginErrors.password = data.errors.password;
            }
          }

          // Загальна помилка
          if (data.error_message) {
            this.loginErrors.general = data.error_message;
          } else if (!this.loginErrors.email && !this.loginErrors.password) {
            this.loginErrors.general = 'Невірний email або пароль';
          }

          // Показуємо помилку через emitter
          emitter.emit(EventTypes.AUTH.LOGIN_ERROR, data.error_message || data.errors);
        }
      } catch (error) {
        this.loginErrors.general = 'Помилка з\'єднання з сервером. Спробуйте пізніше.';
        emitter.emit(EventTypes.AUTH.LOGIN_ERROR, 'Network error');
      } finally {
        this.isSubmitting = false;
      }
    },

    async handleRegister(event) {
      event.preventDefault();

      // Скидаємо попередні помилки
      this.clearRegisterErrors();

      // Валідація на стороні клієнта
      if (!this.registerForm.firstName) {
        this.registerErrors.firstName = 'Ім\'я обов\'язкове';
        return;
      }

      if (!this.registerForm.lastName) {
        this.registerErrors.lastName = 'Прізвище обов\'язкове';
        return;
      }

      if (!this.registerForm.email) {
        this.registerErrors.email = 'Email обов\'язковий';
        return;
      }

      if (!this.registerForm.password) {
        this.registerErrors.password = 'Пароль обов\'язковий';
        return;
      }

      if (this.passwordsDoNotMatch) {
        this.registerErrors.confirmPassword = 'Паролі не співпадають';
        return;
      }

      if (!this.registerForm.agreeTerms) {
        this.registerErrors.agreeTerms = 'Ви повинні погодитись з умовами використання';
        return;
      }

      // Встановлюємо стан завантаження
      this.isSubmitting = true;

      const registerData = {
        first_name: this.registerForm.firstName,
        last_name: this.registerForm.lastName,
        email: this.registerForm.email,
        password: this.registerForm.password,
        confirm_password: this.registerForm.confirmPassword,
        agree_terms: this.registerForm.agreeTerms,
      };

      try {
        const response = await fetch(`/auth/register/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          body: new URLSearchParams(registerData),
        });

        const data = await response.json();

        if (data.success) {
          // Якщо сервер повертає дані користувача після реєстрації
          if (data.user) {
            const userData = {
              name: data.user.name || registerData.name,
              email: data.user.email || registerData.email,
              id: data.user.id || null
            };

            // Зберігаємо дані в localStorage
            localStorage.setItem('userData', JSON.stringify(userData));
            localStorage.setItem('isAuthenticated', 'true');

            // Використовуємо emitter замість this.$emit
            emitter.emit(EventTypes.AUTH.REGISTER_SUCCESS, userData);
          } else {
            // Якщо сервер не повертає дані користувача, емітимо подію без даних
            emitter.emit(EventTypes.AUTH.REGISTER_SUCCESS);
          }

          // Закриваємо модальне вікно
          this.closeModals();
        } else {
          // Обробка помилок від сервера
          if (data.errors) {
            // Якщо сервер повертає об'єкт з помилками для конкретних полів
            if (data.errors.first_name) {
              this.registerErrors.firstName = data.errors.first_name;
            }
            if (data.errors.last_name) {
              this.registerErrors.lastName = data.errors.last_name;
            }
            if (data.errors.email) {
              this.registerErrors.email = data.errors.email;
            }
            if (data.errors.password) {
              this.registerErrors.password = data.errors.password;
            }
            if (data.errors.confirm_password) {
              this.registerErrors.confirmPassword = data.errors.confirm_password;
            }
            if (data.errors.agree_terms) {
              this.registerErrors.agreeTerms = data.errors.agree_terms;
            }
          }

          // Загальна помилка
          if (data.error_message) {
            this.registerErrors.general = data.error_message;
          }

          // Показуємо помилку через emitter
          emitter.emit(EventTypes.AUTH.REGISTER_ERROR, data.error_message || data.errors);
        }
      } catch (error) {
        this.registerErrors.general = 'Помилка з\'єднання з сервером. Спробуйте пізніше.';
        emitter.emit(EventTypes.AUTH.REGISTER_ERROR, 'Network error');
      } finally {
        this.isSubmitting = false;
      }
    },
    redirectToOAuth(provider) {
      if (window.oauthUrls[provider]) {
        window.location.href = window.oauthUrls[provider];
      } else {
        console.error("Unknown OAuth provider");
      }
    },
    getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === name + '=') {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    },
  },
  mounted() {
    emitter.on(EventTypes.AUTH.OPEN_LOGIN_MODAL, () => {
      this.clearLoginErrors();
      this.isLoginModalVisible = true;
      this.isRegisterModalVisible = false;
    });

    emitter.on(EventTypes.AUTH.OPEN_REGISTER_MODAL, () => {
      this.clearRegisterErrors();
      this.isRegisterModalVisible = true;
      this.isLoginModalVisible = false;
    });

    emitter.on(EventTypes.AUTH.CLOSE_AUTH_MODALS, () => {
      this.closeModals();
    });
  },
  beforeUnmount() {
    emitter.off(EventTypes.AUTH.OPEN_LOGIN_MODAL);
    emitter.off(EventTypes.AUTH.OPEN_REGISTER_MODAL);
    emitter.off(EventTypes.AUTH.CLOSE_AUTH_MODALS);
  },
  watch: {
    // Додаємо спостерігачі для очищення помилок при зміні форми
    'loginForm.email': function() {
      this.loginErrors.email = '';
      this.loginErrors.general = '';
    },
    'loginForm.password': function() {
      this.loginErrors.password = '';
      this.loginErrors.general = '';
    },
    'registerForm.firstName': function() {
      this.registerErrors.firstName = '';
      this.registerErrors.general = '';
    },
    'registerForm.lastName': function() {
      this.registerErrors.lastName = '';
      this.registerErrors.general = '';
    },
    'registerForm.email': function() {
      this.registerErrors.email = '';
      this.registerErrors.general = '';
    },
    'registerForm.password': function() {
      this.registerErrors.password = '';
      this.registerErrors.general = '';
    },
    'registerForm.confirmPassword': function() {
      this.registerErrors.confirmPassword = '';
      this.registerErrors.general = '';
    },
    'registerForm.agreeTerms': function() {
      this.registerErrors.agreeTerms = '';
      this.registerErrors.general = '';
    }
  }
}
</script>

<style scoped>
/* Кнопки авторизації на головній сторінці */
.auth-buttons {
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  gap: 10px;
  z-index: 100;
}

.btn-auth {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.btn-login:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.btn-register {
  background: linear-gradient(45deg, var(--color-primary), rgba(108, 99, 255, 0.8));
  border: none;
}

.btn-register:hover {
  box-shadow: 0 0 15px rgba(108, 99, 255, 0.5);
  transform: translateY(-2px);
}

/* Модальне вікно */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.modal-container {
  width: 100%;
  max-width: 500px;
  background: linear-gradient(135deg, rgba(26, 26, 46, 0.95), rgba(20, 20, 35, 0.95));
  border-radius: 16px;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
  animation: slideUp 0.4s ease;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-title {
  color: white;
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
  background: linear-gradient(45deg, #fff, rgba(255, 255, 255, 0.7));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.modal-close {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  padding: 5px;
  transition: all 0.3s ease;
  border-radius: 50%;
}

.modal-close:hover {
  color: white;
  background: rgba(255, 255, 255, 0.1);
}

.modal-body {
  padding: 25px;
}

/* Форма */
.form-group {
  margin-bottom: 20px;
}

.form-row {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.form-row .form-group {
  flex: 1;
  margin-bottom: 0;
}

label {
  display: block;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 12px;
  color: rgba(108, 99, 255, 0.7);
}

.form-input {
  width: 100%;
  padding: 12px 12px 12px 40px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: white;
  font-size: 15px;
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(108, 99, 255, 0.3);
  background: rgba(255, 255, 255, 0.08);
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

.password-toggle {
  position: absolute;
  right: 12px;
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  padding: 0;
}

.password-toggle:hover {
  color: white;
}

.input-error {
  border-color: #ff4757 !important;
  box-shadow: 0 0 0 2px rgba(255, 71, 87, 0.3) !important;
}

.input-wrapper.has-error .form-input {
  border-color: #ff4757;
  box-shadow: 0 0 0 2px rgba(255, 71, 87, 0.3);
}

/* Стилі для повідомлень про помилки */
.form-error {
  color: #ff4757;
  font-size: 12px;
  margin-top: 5px;
}

.general-error {
  background: rgba(255, 71, 87, 0.1);
  border: 1px solid rgba(255, 71, 87, 0.3);
  border-radius: 8px;
  padding: 10px;
  margin-bottom: 15px;
  font-size: 14px;
  text-align: center;
}

/* Анімації для повідомлень про помилки */
.fade-slide-up-enter-active,
.fade-slide-up-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-up-enter-from,
.fade-slide-up-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

.fade-slide-down-enter-active,
.fade-slide-down-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-down-enter-from,
.fade-slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Стилі для індикатора завантаження */
.spinner {
  animation: rotate 2s linear infinite;
  width: 18px;
  height: 18px;
  margin-right: 8px;
  vertical-align: middle;
}

.spinner .path {
  stroke: white;
  stroke-linecap: round;
  animation: dash 1.5s ease-in-out infinite;
}

@keyframes rotate {
  100% {
    transform: rotate(360deg);
  }
}

@keyframes dash {
  0% {
    stroke-dasharray: 1, 150;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -35;
  }
  100% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -124;
  }
}

.password-strength {
  margin-top: 10px;
}

.strength-meter {
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 5px;
}

.strength-bar {
  height: 100%;
  border-radius: 2px;
  transition: all 0.3s ease;
}

.strength-text {
  font-size: 12px;
  text-align: right;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  flex-wrap: wrap;
  gap: 10px;
}

.checkbox-container {
  display: flex;
  align-items: center;
  position: relative;
  padding-left: 30px;
  cursor: pointer;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  user-select: none;
}

.checkbox-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkmark {
  position: absolute;
  top: 0;
  left: 0;
  height: 20px;
  width: 20px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}

.checkbox-container:hover input ~ .checkmark {
  background: rgba(255, 255, 255, 0.1);
}

.checkbox-container input:checked ~ .checkmark {
  background: var(--color-primary);
  border-color: var(--color-primary);
}

.checkmark:after {
  content: "";
  position: absolute;
  display: none;
}

.checkbox-container input:checked ~ .checkmark:after {
  display: block;
}

.checkbox-container .checkmark:after {
  left: 7px;
  top: 3px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.forgot-password {
  color: var(--color-primary);
  text-decoration: none;
  font-size: 14px;
  transition: all 0.3s ease;
}

.forgot-password:hover {
  text-decoration: underline;
}

.btn-submit {
  width: 100%;
  padding: 14px;
  background: linear-gradient(45deg, var(--color-primary), rgba(108, 99, 255, 0.8));
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.btn-submit:hover {
  box-shadow: 0 0 20px rgba(108, 99, 255, 0.5);
  transform: translateY(-2px);
}

.btn-submit:disabled {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.5);
  cursor: not-allowed;
  box-shadow: none;
  transform: none;
}

.btn-particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  pointer-events: none;
}

/* Соціальні кнопки */
.social-login {
  margin-top: 30px;
  text-align: center;
}

.social-login p {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  margin-bottom: 15px;
  position: relative;
}

.social-login p:before,
.social-login p:after {
  content: "";
  position: absolute;
  top: 50%;
  width: 25%;
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
}

.social-login p:before {
  left: 0;
}

.social-login p:after {
  right: 0;
}

.social-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.social-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 10px 20px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.05);
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.social-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.social-btn.google {
  color: #ea4335;
}

.social-btn.facebook {
  color: #1877f2;
}

/* Футер модального вікна */
.modal-footer {
  margin-top: 25px;
  text-align: center;
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
}

.modal-footer a {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.modal-footer a:hover {
  text-decoration: underline;
}

/* Анімації */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { transform: translateY(30px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

/* Адаптивність */
@media (max-width: 576px) {
  .modal-container {
    width: 90%;
  }

  .form-row {
    flex-direction: column;
    gap: 20px;
  }

  .form-options {
    flex-direction: column;
    align-items: flex-start;
  }

  .social-buttons {
    flex-direction: column;
  }
}
</style>