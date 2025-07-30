<template>

  <head>
    <title>
      Pharmacy Council Drug Registration Form
    </title>
    <link rel="icon" href="../assets/cardtp-small.png" type="image/x-icon">
  </head>
  <div class="container">
    <img src="../assets/coat-of-arms.png" alt="Coat of Arms" class="coat-of-arms" />
    <img src="../assets/cardtp.png" alt="CardTP Logo" class="cardtp-logo" />
    <img src="../assets/vswift.png" alt="vswift" class="vswift" />
    
    <h1>Pharmacy Council Drug Registration Form</h1>
    <form @submit.prevent="handleSubmit" class="form">
      <div class="form-group">
        <label for="fullName">Full Name:</label>
        <input type="text" id="fullName" v-model="formData.fullName" required />
      </div>
      <div class="form-group">
        <label for="pharmacyName">Name of Pharmacy:</label>
        <input type="text" id="pharmacyName" v-model="formData.pharmacyName" required  />
      </div>
      <div class="form-group">
        <label for="businessAddress">Business Address:</label>
        <input type="text" id="businessAddress" v-model="formData.businessAddress" required />
      </div>

      <h2>Drug Details</h2>
      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th>Brand Name</th>
              <th>Dosage Form</th>
              <th>Strength</th>
              <th>Manufacturer Name</th>
              <th>Manufacturer Address</th>
              <th>Notes</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, index) in tableData" :key="index">
              <td><textarea v-model="row.brandName" rows="1" @input="autoResize($event)"></textarea></td>
              <td><textarea v-model="row.dosageForm" rows="1" @input="autoResize($event)"></textarea></td>
              <td><textarea v-model="row.strength" rows="1" @input="autoResize($event)"></textarea></td>
              <td><textarea v-model="row.manufacturerName" rows="1" @input="autoResize($event)"></textarea></td>
              <td><textarea v-model="row.manufacturerAddress" rows="1" @input="autoResize($event)"></textarea></td>
              <td><textarea v-model="row.notes" rows="1" @input="autoResize($event)"></textarea></td>
            </tr>
          </tbody>
        </table>
      </div>
      <button @click="addRow" type="button" class="add-row-button">Add Row</button>
      <button type="submit" class="submit-button">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { reactive } from 'vue';
import axios from 'axios';
import { useFavicon } from '@vueuse/core';

const icon = useFavicon();
icon.value = "../assets/cardtp-small.png;" // Path to your favicon

const formData = reactive({
  fullName: '',
  pharmacyName: '',
  businessAddress: '',
});

const tableData = reactive([
  {
    brandName: '',
    dosageForm: '',
    strength: '',
    manufacturerName: '',
    manufacturerAddress: '',
    notes: '',
  },
]);

const addRow = () => {
  tableData.push({
    brandName: '',
    dosageForm: '',
    strength: '',
    manufacturerName: '',
    manufacturerAddress: '',
    notes: '',
  });
};

const autoResize = (event) => {
  const textarea = event.target;
  textarea.style.height = 'auto'; // Reset height to calculate new height
  textarea.style.height = `${textarea.scrollHeight}px`; // Set height based on content
};

const handleSubmit = async () => {
  const submissionData = {
    full_name: formData.fullName,
    pharmacy_name: formData.pharmacyName,
    business_address: formData.businessAddress,
    drug_details: tableData.map(row => ({
      brand_name: row.brandName,
      dosage_form: row.dosageForm,
      strength: row.strength,
      manufacturer_name: row.manufacturerName,
      manufacturer_address: row.manufacturerAddress,
      notes: row.notes,
    })),
  };

  try {
    const response = await axios.post('http://10.1.181.116:8000/submit', submissionData);
    console.log('Submission successful:', response.data);
    alert('Form submitted successfully!');
  } catch (error) {
    console.error('Error submitting form:', error);
    alert('Failed to submit the form. Please try again.');
  }
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  position: relative; /* Ensure positioning for the logos */
  text-align: center; /* Center-align content */
}

.coat-of-arms {
  position: relative;
  display: inline-block; /* Allow logos to be inline */
  width: 65px; /* Adjust size as needed */
  height: auto;
  margin-right: 40px; /* Increase spacing between logos */
  vertical-align: middle; /* Align middle of logo */
}

.cardtp-logo {
  position: relative;
  display: inline-block; /* Allow logos to be inline */
  width: 200px; /* Adjust size as needed */
  height: auto;
  margin-left: 40px; /* Increase spacing between logos */
  margin-right: 40px; /* Increase spacing between logos */
  vertical-align: middle; /* Align middle of logo */
}

.vswift {
  position: relative;
  display: inline-block; /* Allow logos to be inline */
  width: 180px; /* Adjust size as needed */
  height: auto;
  margin-left: -2rem; /* Increase spacing between logos */
  vertical-align: middle; /* Align middle of logo */
}

h1 {
  margin-top: 50px; /* Move heading text down */
  color: #333;
  font-size: 24px;
  text-align: center;
}

.form {
  margin-top: 20px; /* Add spacing between heading and form */
}

.form-group {
  margin-bottom: 15px;
  padding: 3px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  resize: none; /* Prevent manual resizing */
  overflow-wrap: break-word; /* Ensure text wraps properly */
  word-wrap: break-word;
  word-break: break-word;
}

.submit-button, .add-row-button {
  display: block;
  margin: 10px auto;
  padding: 10px 20px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.submit-button:hover, .add-row-button:hover {
  background-color: #0056b3;
}

.table-container {
  height: 160px; /* Increased height for the table container */
  overflow-y: auto; /* Enable vertical scrolling for overflow content */
  border: 1px solid #ddd; /* Add a border around the container */
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th, .table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
  vertical-align: top;
}

.table th {
  background-color: #f4f4f4;
  font-weight: bold;
}

#pharmacyName, #businessAddress, #fullName {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  font-size: medium;
  font-family: Arial, sans-serif;
}
</style>