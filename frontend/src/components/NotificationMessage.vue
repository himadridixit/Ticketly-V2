<template>
  <div class="notification-message" :class="{'show': show}">
    {{ message }}
  </div>
</template>

<script>
export default {
  props: {
    message: String,
    duration: {
      type: Number,
      default: 3000, // Default duration in milliseconds (3 seconds)
    },
  },
  data() {
    return {
      show: false,
    };
  },
  watch: {
    message(newMessage) {
      this.showMessage(newMessage);
    },
  },
  methods: {
    showMessage(message) {
      this.show = true;
      setTimeout(() => {
        this.show = false;
      }, this.duration);
    },
  },
};
</script>

<style>
.notification-message {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #333;
  color: #fff;
  padding: 10px 20px;
  border-radius: 4px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.notification-message.show {
  opacity: 1;
}
</style>
