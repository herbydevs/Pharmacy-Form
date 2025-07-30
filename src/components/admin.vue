<template>
  <div class="container" v-if="isLoggedIn">
    <h1>Admin View</h1>
    <button @click="downloadExcel" class="download-button">Download as Excel</button>
    <table class="table">
      <thead>
        <tr>
          <th>Full Name</th>
          <th>Pharmacy Name</th>
          <th>Business Address</th>
          <th>Brand Name</th>
          <th>Dosage Form</th>
          <th>Strength</th>
          <th>Manufacturer Name</th>
          <th>Manufacturer Address</th>
          <th>Notes</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="(entry, index) in sortedFormEntries" :key="index">
          <tr v-for="(drug, drugIndex) in entry.sortedDrugDetails" :key="drugIndex">
            <td v-if="drugIndex === 0" :rowspan="entry.sortedDrugDetails.length">{{ entry.full_name }}</td>
            <td v-if="drugIndex === 0" :rowspan="entry.sortedDrugDetails.length">{{ entry.pharmacy_name }}</td>
            <td v-if="drugIndex === 0" :rowspan="entry.sortedDrugDetails.length">{{ entry.business_address }}</td>
            <td>{{ drug.brand_name }}</td>
            <td>{{ drug.dosage_form }}</td>
            <td>{{ drug.strength }}</td>
            <td>{{ drug.manufacturer_name }}</td>
            <td>{{ drug.manufacturer_address }}</td>
            <td>{{ drug.notes }}</td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
  <div v-else>
    <div class="login-container" v-if="!isLoggedIn">
    <h1>Admin Login</h1>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="username">Username:</label>
        <input v-model="username" id="username" type="text" required />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input v-model="password" id="password" type="password" required />
      </div>
      <button type="submit" class="login-button">Login</button>
      <p v-if="loginError" class="error">{{ loginError }}</p>
    </form>
  </div>
  <div v-else>
    <h2>Welcome, {{ username }}!</h2>
    <button @click="logout" class="logout-button">Logout</button>
    <p class="success">You are now logged in as admin.</p>
    <!-- You can add your admin content here -->
  </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import * as XLSX from 'xlsx';

const formEntries = ref([]);


const fetchFormEntries = async () => {
  try {
    const response = await axios.get('https://learnvswift.gov.vc/api/entries'); // Adjust the URL as needed
    formEntries.value = response.data;
  } catch (error) {
    console.error('Error fetching form entries:', error);
  }
};

const sortedFormEntries = computed(() => {
  return formEntries.value
    .map(entry => ({
      ...entry,
      sortedDrugDetails: entry.drug_details.sort((a, b) => a.brand_name.localeCompare(b.brand_name)),
    }))
    .sort((a, b) => a.full_name.localeCompare(b.full_name));
});

const downloadExcel = () => {
  const data = sortedFormEntries.value.flatMap(entry =>
    entry.sortedDrugDetails.map(drug => ({
      FullName: entry.full_name,
      PharmacyName: entry.pharmacy_name,
      BusinessAddress: entry.business_address,
      BrandName: drug.brand_name,
      DosageForm: drug.dosage_form,
      Strength: drug.strength,
      ManufacturerName: drug.manufacturer_name,
      ManufacturerAddress: drug.manufacturer_address,
      Notes: drug.notes,
    }))
  );

  const worksheet = XLSX.utils.json_to_sheet(data);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Form Entries');
  XLSX.writeFile(workbook, 'FormEntries.xlsx');
};

onMounted(() => {
  fetchFormEntries();
});


const validUsers = [
  { username: 'admin', password: 'woohooitsme' },
  { username: 'superman', password: 'supersecret' },
  // Add more users as needed
];

const username = ref('');
const password = ref('');
const isLoggedIn = ref(false);
const loginError = ref('');

function handleLogin() {
  const found = validUsers.find(
    user => user.username === username.value && user.password === password.value
  );
  if (found) {
    isLoggedIn.value = true;
    loginError.value = '';
  } else {
    loginError.value = 'Invalid username or password.';
  }
}

function logout() {
  isLoggedIn.value = false;
  username.value = '';
  password.value = '';
  loginError.value = '';
}

</script>

<style scoped>
.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  color: #333;
  font-size: 24px;
  margin-bottom: 20px;
}

.download-button {
  display: block;
  margin: 10px auto 20px;
  padding: 10px 20px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.download-button:hover {
  background-color: #218838;
}

.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.table th, .table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
  font-size: 14px;
}

.table th {
  background-color: #007BFF;
  color: white;
  font-weight: bold;
}

.table tr:nth-child(even) {
  background-color: #f2f2f2;
}

.table tr:hover {
  background-color: #e6f7ff;
}

.table td {
  vertical-align: top;
}


.login-container {
  max-width: 400px;
  margin: 60px auto;
  padding: 32px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  font-family: Arial, sans-serif;
}

h1 {
  text-align: center;
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 18px;
}

label {
  display: block;
  margin-bottom: 6px;
  font-weight: bold;
}

input[type="text"], input[type="password"] {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 15px;
}

.login-button, .logout-button {
  width: 100%;
  padding: 10px;
  background: #007BFF;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 8px;
}

.login-button:hover, .logout-button:hover {
  background: #0056b3;
}

.error {
  color: #d32f2f;
  margin-top: 12px;
  text-align: center;
}

.success {
  color: #388e3c;
  margin-top: 18px;
  text-align: center;
}
</style>