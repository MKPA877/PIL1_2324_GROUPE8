<template>
    <div>
        <h1>Login Page</h1>
        <form @submit.prevent="login">
            <input v-model="username" placeholder="Username">
            <input v-model="password" type="password" placeholder="Password">
            <button type="submit">Login</button>
        </form>
    </div>
</template>

<script>
export default {
    data() {
        return {
            username: '',
            password: ''
        }
    },
    methods: {
        login() {
            // Handle login logic
        }
    }
}
</script>
