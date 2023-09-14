<template>
    <div class="flex-grow-1 p-2">
        <div class="p-2">
                <BookingsList v-for="booking in bookings" :key="booking.booking_id" :booking="booking" />
        </div>
    </div>

</template>

<script>
    import BookingsList from '@/components/BookingsList.vue'
    import { mapActions } from "vuex";
    export default {
        name: "bookinglist",
        components: {
            BookingsList
        },
        computed: {
                bookings: function () {
                return this.$store.getters.bookings;
                }
        },
        methods: {
            ...mapActions(["getBookings"])
        },
        created: function() {
          this.getBookings();
        }
    }
</script>