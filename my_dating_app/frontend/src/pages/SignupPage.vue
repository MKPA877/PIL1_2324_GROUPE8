<template>
    <div>
        <h1>Signup Page</h1>
        <form @submit.prevent="signup">
            <input v-model="username" placeholder="Username">
            <input v-model="password" type="password" placeholder="Password">
            <button type="submit">Signup</button>
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
        signup() {
            // Handle signup logic
        }
    }
}
</script>
