<template>
  <div class="cart-container">
    <!-- Header -->
    <div class="header-section">
      <h1 class="page-title">🛒 Giỏ Hàng Của Bạn</h1>
      <p class="page-subtitle">Kiểm tra sản phẩm và hoàn tất thông tin đặt hàng</p>
    </div>

    <!-- Khi giỏ trống -->
    <div v-if="!hasProducts" class="empty-state">
      <div class="empty-card">
        <p class="empty-icon">🛍️</p>
        <h2>Giỏ hàng trống</h2>
        <p>Bạn chưa có sản phẩm nào trong giỏ hàng.</p>
        <button @click="mockAddProduct" class="btn-primary">Tiếp tục mua sắm</button>
      </div>
    </div>

    <!-- Khi có sản phẩm -->
    <div v-else class="cart-content">
      <!-- Bên trái: Sản phẩm -->
      <div class="left-panel glass-card">
        <h2 class="section-title">Sản phẩm ({{ cartItems.length }})</h2>

        <div class="product-list">
          <div v-for="(product, i) in cartItems" :key="i" class="product-item">
            <input type="checkbox" v-model="product.selected" class="product-checkbox" />

            <img :src="product.img" alt="" class="product-image" />
            <div class="product-info">
              <h3 class="product-name">{{ product.productName }}</h3>
              <div class="product-selects">
                <span class="select-sm">
                  {{ product.productAttName }}
                </span>
                <span class="select-sm">
                  {{ product.color }}
                </span>
              </div>

              <div class="price-row">
                <p>
                  Giá: <strong>{{ formatPrice(product.price) }}</strong>
                </p>
              </div>

              <div class="qty-row">
                <label>Số lượng:</label>
                <div class="qty-control">
                  <button type="button" class="qty-btn" @click="decreaseQty(product)">−</button>
                  <input
                    type="number"
                    v-model.number="product.quantity"
                    min="1"
                    class="qty-input"
                  />
                  <button type="button" class="qty-btn" @click="increaseQty(product)">+</button>
                </div>
              </div>
            </div>

            <button @click="removeCartItem(product.id)" class="btn-remove">🗑️</button>
          </div>
        </div>

        <div class="price-summary">
          <p>
            Tổng cộng: <strong class="total-price">{{ formatPrice(totalPrice) }}</strong>
          </p>
        </div>
      </div>

      <!-- Bên phải: Form đặt hàng -->
      <div class="right-panel glass-card">
        <h2 class="section-title">Thông tin đặt hàng</h2>

        <form @submit.prevent="handleSubmit" class="order-form">
          <div class="form-group">
            <label>Họ và tên *</label>
            <input required v-model.trim="form.fullName" type="text" class="form-input" />
            <span v-if="errors.fullName" class="error-text">{{ errors.fullName }}</span>
          </div>

          <div class="form-group">
            <label>Số điện thoại *</label>
            <input required v-model.trim="form.phoneNumber" type="tel" class="form-input" />
            <span v-if="errors.phoneNumber" class="error-text">{{ errors.phoneNumber }}</span>
          </div>

          <div class="form-group">
            <label>Email *</label>
            <input v-model.trim="form.email" type="text" class="form-input" />
            <span v-if="errors.email" class="error-text">{{ errors.email }}</span>
          </div>

          <!-- <div class="form-group">
            <label>Hình thức nhận hàng *</label>
            <select v-model="form.deliveryMethod" class="form-input">
              <option value="">-- Chọn hình thức --</option>
              <option value="home">Giao hàng tại nhà</option>
              <option value="store">Nhận tại cửa hàng</option>
            </select>
            <span v-if="errors.deliveryMethod" class="error-text">{{ errors.deliveryMethod }}</span>
          </div> -->

          <div  class="form-group">
            <label>Địa chỉ nhận hàng *</label>
            <textarea v-model.trim="form.address" class="form-input" rows="3"></textarea>
            <span v-if="errors.address" class="error-text">{{ errors.address }}</span>
          </div>

          <div class="form-group">
            <label>Ghi chú (tùy chọn)</label>
            <textarea v-model.trim="form.description" class="form-input" rows="2"></textarea>
          </div>

          <div class="form-group checkbox-row">
            <input type="checkbox" v-model="form.invoiceEmail" />
            <label>Xuất hóa đơn qua email</label>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-primary">
              Xác nhận & Đặt hàng
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Confirm dialog -->
    <div v-if="showConfirm" class="confirm-overlay">
      <div class="confirm-dialog glass-card">
        <h3>Xác nhận đặt hàng</h3>
        <p>Bạn có chắc muốn đặt {{ selectedCount }} sản phẩm?</p>
        <div class="confirm-actions">
          <button @click="confirmOrder" class="btn-primary">Đặt hàng</button>
          <button @click="showConfirm = false" class="btn-cancel">Hủy</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const hasProducts = ref(true)
const showConfirm = ref(false)
const router = useRouter()

const cartItems = ref([])
const form = ref({
  fullName: '',
  phoneNumber: '',
  email: '',
  address: '',
  description: '',
  items: [],
})
const errors = ref({})
const handleFetchCart = async () => {
  const token = localStorage.getItem('token')
  if (!token) return router.push('/login')
  try {
    const [cartResponse, userDataRes] = await Promise.all([
      axios.get('http://localhost:8080/bej3/cart/view', {
        headers: { Authorization: `Bearer ${token}` },
      }),
      axios.get('http://localhost:8080/bej3/users/profile/my-info', {
        headers: { Authorization: `Bearer ${token}` },
      }),
    ])
    form.value = {
      ...form.value,
      fullName: userDataRes.data.result?.fullName || '',
      phoneNumber: userDataRes.data.result?.phoneNumber || '',
      email: userDataRes.data.result?.email || '',
      address: userDataRes.data.result?.address || '',
    }
    cartItems.value = cartResponse.data.result
      .map((item) => ({ ...item, selected: Boolean(item.selected), quantity: Number(item.quantity) || 1 }))
    hasProducts.value = cartItems.value.length > 0
  } catch (error) {
    console.error('Lỗi khi tải giỏ hàng:', error)
    alert('Không thể tải giỏ hàng!')
  }
}
onMounted(() => {
  handleFetchCart()
})
const handlePlaceOrder = async () => {
  const token = localStorage.getItem('token')
  if (!token) return router.push('/login')

  const selectedItems = cartItems.value.filter((p) => p.selected)

  if (selectedItems.length === 0) {
    alert('Vui lòng chọn ít nhất một sản phẩm để đặt hàng.')
    return
  }

  try {
    // Gán danh sách sản phẩm đã chọn vào form
    const orderData = {
      type: 0,
      description: form.value.description,
      address: form.value.address,
      email: form.value.email,
      phoneNumber: form.value.phoneNumber,
      items: selectedItems
        .map((p) => ({
          productAttId: p.attId,
          cartItemId: p.id,
          quantity: Number(p.quantity),
        })),
    }

    console.log('Order data gửi lên:', JSON.stringify(orderData, null, 2))
    await axios.post('http://localhost:8080/bej3/cart/place-order', orderData, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    alert('Đặt hàng thành công!')
    cartItems.value = cartItems.value.filter((p) => !p.selected)
    hasProducts.value = cartItems.value.length > 0
  } catch (error) {
    console.error('Lỗi khi đặt hàng:', error)
    alert('Không thể đặt hàng!')
  }
}


// ============================================== remove item ===========================
const removeCartItem = async (cartItemId) => {
  const token = localStorage.getItem('token')
  if (!token) {
    router.push('/login')
    return
  }

  try {
    await axios.delete(`http://localhost:8080/bej3/cart/remove/${cartItemId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    handleFetchCart()
  } catch (error) {
    console.error('Lỗi', error)
    alert('Failed to fetch orders!!!!')

    if (error.response && (error.response.status === 401 || error.response.status === 500)) {
      localStorage.removeItem('token')
      router.push('/login')
    }
  }
}
// ============================================= ==============================================

const formatPrice = (v) =>
  new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(v)

const totalPrice = computed(() =>
  cartItems.value.filter((p) => p.selected).reduce((sum, p) => sum + p.price * p.quantity, 0),
)

const selectedCount = computed(() => cartItems.value.filter((p) => p.selected).length)

const increaseQty = (p) => (p.quantity += 1)
const decreaseQty = (p) => (p.quantity = Math.max(1, p.quantity - 1))

const validateForm = () => {
  const e = {}
  if (!form.value.fullName) e.fullName = 'Vui lòng nhập họ tên'
  if (!form.value.phoneNumber) e.phoneNumber = 'Vui lòng nhập số điện thoại'
  if (!form.value.email) e.email = 'Vui lòng nhập email'
  if (!form.value.address) e.address = 'Vui lòng nhập địa chỉ giao hàng'
  errors.value = e
  return Object.keys(e).length === 0
}

const handleSubmit = () => {
  if (!validateForm()) return
  if (selectedCount.value === 0) {
    alert('Vui lòng chọn ít nhất 1 sản phẩm để đặt hàng')
    return
  }
  showConfirm.value = true
}

const confirmOrder = async () => {
  showConfirm.value = false
  await handlePlaceOrder()
}

const mockAddProduct = () => (hasProducts.value = true)
</script>

//=============================== Styles ====================================
<style scoped>
.cart-container {
  min-height: 100vh;
  background: #ffffff;
  padding: 2rem;
  font-family: 'Inter', sans-serif;
}

.header-section {
  text-align: center;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #0369a1;
}

.page-subtitle {
  color: #64748b;
}

/* Giỏ trống */
.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 60vh;
}

.empty-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  padding: 3rem 4rem;
  text-align: center;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

/* Layout */
.cart-content {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: 2rem;
}

.glass-card {
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(0, 0, 0, 0.05);
  border-radius: 16px;
  padding: 1.5rem;
  backdrop-filter: blur(12px);
}

.section-title {
  font-weight: 600;
  font-size: 1.25rem;
  color: #0369a1;
  margin-bottom: 1rem;
}

/* Sản phẩm */
.product-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.product-item {
  display: flex;
  gap: 1rem;
  align-items: center;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 1rem;
}

.product-checkbox {
  accent-color: #0ea5e9;
}

.product-image {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  object-fit: contain;
}

.product-info {
  flex: 1;
}

.product-selects {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.select-sm {
  padding: 0.4rem 0.75rem;
  border-radius: 6px;
  border: 1px solid #cbd5e1;
  background: #fff;
  font-size: 0.9rem;
}

.qty-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.25rem;
}

.qty-control {
  display: flex;
  align-items: center;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  overflow: hidden;
}

.qty-btn {
  background: #f1f5f9;
  border: none;
  padding: 0.4rem 0.7rem;
  cursor: pointer;
  font-size: 1rem;
  color: #0369a1;
}

.qty-input {
  width: 45px;
  text-align: center;
  border: none;
  font-size: 1rem;
}

.btn-remove {
  border: none;
  background: transparent;
  cursor: pointer;
  color: #ef4444;
  font-size: 1.2rem;
}

/* Tổng giá */
.price-summary {
  text-align: right;
  margin-top: 1.5rem;
  font-weight: 600;
  color: #0369a1;
}

.total-price {
  color: #0ea5e9;
  font-size: 1.25rem;
}

/* Form */
.form-group {
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
}

.form-input {
  border-radius: 8px;
  border: 1px solid #cbd5e1;
  padding: 0.75rem 1rem;
  font-size: 0.95rem;
}

.form-input:focus {
  outline: none;
  border-color: #0ea5e9;
  box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.25);
}

.checkbox-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.error-text {
  font-size: 0.85rem;
  color: #ef4444;
  margin-top: 4px;
}

/* Nút */
.form-actions {
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
}

.btn-primary {
  background: linear-gradient(135deg, #0ea5e9, #06b6d4);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.9rem 1.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  background: linear-gradient(135deg, #0284c7, #0891b2);
}

.btn-cancel {
  background: #e2e8f0;
  border: none;
  border-radius: 8px;
  padding: 0.8rem 1.2rem;
  cursor: pointer;
  font-weight: 500;
}

/* Confirm dialog */
.confirm-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(15, 23, 42, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
}

.confirm-dialog {
  width: 320px;
  text-align: center;
}

.confirm-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.5rem;
}
</style>
