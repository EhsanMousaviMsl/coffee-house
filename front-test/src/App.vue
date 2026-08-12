<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const items = ref([])
const errorMessage = ref('')
const isLoading = ref(true)

// Fallback high-quality images based on coffee product names
const getCoffeeImage = (item) => {
  if (item.image_url && item.image_url !== 'string' && item.image_url.startsWith('http')) {
    return item.image_url
  }
  
  const name = item.name.toLowerCase()
  if (name.includes('latte')) return 'https://unsplash.com'
  if (name.includes('espresso')) return 'https://unsplash.com'
  if (name.includes('macchiato')) return 'https://unsplash.com'
  if (name.includes('americano')) return 'https://unsplash.com'
  if (name.includes('mocha')) return 'https://unsplash.com'
  
  // Generic beautiful coffee fallback image
  return 'https://unsplash.com'
}

const fetchBackendData = async () => {
  try {
    isLoading.value = true
    const response = await axios.get('http://localhost:8000/api/v1/products/')
    items.value = response.data
    errorMessage.value = ''
  } catch (error) {
    errorMessage.value = 'Failed to load the menu. Please check your server connection.'
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchBackendData()
})
</script>

<template>
  <div style="background-color: #12100e; color: #f4f1ea; min-h: 100vh; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0;">
    
    <!-- Hero Banner Component -->
    <div style="background: linear-gradient(rgba(18, 16, 14, 0.6), #12100e), url('https://unsplash.com') center/cover; padding: 100px 20px; text-align: center;">
      <h1 style="font-size: 3.5rem; margin: 0 0 10px 0; font-family: Georgia, serif; color: #d4a373; letter-spacing: 2px;">THE ROASTERY</h1>
      <p style="font-size: 1.2rem; color: #dddddd; max-width: 600px; margin: 0 auto 30px auto; font-style: italic;">
        Experience exceptionally crafted espresso drinks brewed with beans roasted fresh in-house daily.
      </p>
      <button @click="fetchBackendData" style="background-color: #d4a373; color: #12100e; border: none; padding: 12px 28px; border-radius: 30px; font-weight: bold; cursor: pointer; transition: 0.2s; font-size: 1rem;">
        Refresh Live Menu
      </button>
    </div>

    <!-- Main Content Architecture Area -->
    <div style="max-width: 1100px; margin: 0 auto; padding: 40px 20px;">
      
      <!-- Feedback States -->
      <div v-if="isLoading" style="text-align: center; font-size: 1.2rem; color: #a49e95; padding: 60px 0;">
        Preparing the menu boards...
      </div>

      <div v-else-if="errorMessage" style="background-color: #3a1c1c; border-left: 4px solid #f87171; color: #fca5a5; padding: 20px; border-radius: 6px; margin-bottom: 30px;">
        {{ errorMessage }}
      </div>

      <!-- Menu Grid Architecture -->
      <div v-else>
        <div style="border-bottom: 1px solid #2a241f; padding-bottom: 15px; margin-bottom: 35px; display: flex; justify-content: space-between; align-items: baseline;">
          <h2 style="font-size: 2rem; font-family: Georgia, serif; color: #d4a373; margin: 0;">Our Craft Brews</h2>
          <span style="color: #a49e95; font-size: 0.9rem;">{{ items.length }} seasonal options available</span>
        </div>

        <div v-if="items.length === 0" style="text-align: center; padding: 60px; color: #a49e95; border: 1px dashed #2a241f; border-radius: 12px;">
          No custom creations found on the server.
        </div>

        <!-- Responsive Card Grid Setup -->
        <div v-else style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 30px;">
          <div v-for="item in items" :key="item.id" style="background-color: #1c1814; border: 1px solid #2a241f; border-radius: 12px; overflow: hidden; display: flex; flex-direction: column; transition: transform 0.2s; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
            
            <!-- Graphic Image Wrapper -->
            <div style="position: relative; height: 200px; width: 100%; overflow: hidden;">
              <img :src="getCoffeeImage(item)" :alt="item.name" style="width: 100%; height: 100%; object-fit: cover;" />
              
              <!-- Clean Availability Badge Overlay -->
              <span :style="{
                position: 'absolute',
                top: '15px',
                right: '15px',
                fontSize: '0.75rem',
                padding: '5px 10px',
                borderRadius: '20px',
                fontWeight: 'bold',
                textTransform: 'uppercase',
                backgroundColor: item.available && item.inventory > 0 ? '#1b4332' : '#4a1515',
                color: item.available && item.inventory > 0 ? '#d8f3dc' : '#fecdd3'
              }">
                {{ item.available && item.inventory > 0 ? 'Available' : 'Sold Out' }}
              </span>
            </div>

            <!-- Descriptive Text Body -->
            <div style="padding: 20px; flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 10px;">
                  <h3 style="margin: 0; font-size: 1.4rem; font-family: Georgia, serif; color: #f4f1ea;">{{ item.name }}</h3>
                  <span style="font-size: 1.3rem; font-weight: bold; color: #d4a373;">
                    ${{ parseFloat(item.price).toFixed(2) }}
                  </span>
                </div>
                <p style="margin: 0 0 20px 0; color: #a49e95; font-size: 0.95rem; line-height: 1.5; min-height: 45px;">
                  {{ item.description }}
                </p>
              </div>

              <!-- Footer Metadata Component -->
              <div style="border-top: 1px solid #2a241f; padding-top: 15px; display: flex; justify-content: space-between; align-items: center; font-size: 0.85rem; color: #7c756c;">
                <span>Category ID: <strong>{{ item.category_id }}</strong></span>
                <span>In Stock: <strong :style="{ color: item.inventory > 0 ? '#d4a373' : '#ef4444' }">{{ item.inventory }} units</strong></span>
              </div>
            </div>

          </div>
        </div>

      </div>
    </div>
  </div>
</template>
