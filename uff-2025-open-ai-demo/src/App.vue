<template>
  <div class="my-8 flex justify-center px-4 sm:px-8">
    <div class="bg-white bg-opacity-80 rounded-2xl shadow-2xl p-8 w-full h-full max-h-screen flex flex-col max-w-7xl">
      
      <h1 class="text-3xl font-bold mb-8 text-center text-gray-800">U:FF 2025</h1>
      <h2 class="text-2xl font-bold mb-4 text-center text-gray-800">Offener KI-Chatbot</h2>
      
      <div class="mb-6">
        <label for="model" class="block mb-2 text-xl font-bold text-gray-800">Modell</label>
        <select v-model="selectedModel" class="border border-gray-300 rounded-lg w-full p-4 text-gray-700 focus:outline-none focus:ring-4 focus:ring-purple-400">
          <option v-for="model in models" :key="model.id" :value="model.id">
            {{ model.name }}
          </option>
        </select>
      </div>

      <div class="border border-gray-300 rounded-lg p-6 flex-1 overflow-y-auto mb-6">
        <div v-for="(msg, index) in messages" :key="index" class="mb-4">
          <div :class="msg.role === 'user' ? 'flex justify-end' : 'flex justify-start'">
            <div 
              :class="msg.role === 'user' ? 'text-white p-3 rounded-xl max-w-4xl' : 'text-black p-3 rounded-xl max-w-4xl'" 
              :style="msg.role === 'user' ? 'background-color: #ff5b6a;' : 'background-color: #8000d7; color: white;'"
            >
              <div class="font-bold text-lg mb-1">
                {{ msg.role === 'user' ? 'Ich' : `Modell (${msg.model})` }}
              </div>
              <div class="break-words">
                {{ msg.content }}
              </div>
            </div>
          </div>
        </div>  
      </div>

      <form @submit.prevent="sendMessage" class="flex gap-4">
        <input v-model="newMessage" type="text" class="flex-1 border border-gray-300 rounded-full p-4 focus:outline-none focus:ring-4 focus:ring-purple-400" placeholder="Type a message..." required />
        <button type="submit" class="bg-purple-600 hover:bg-purple-700 text-white font-bold px-6 py-3 rounded-full transition">Senden</button>
      </form>

    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      models: [],
      selectedModel: '',
      messages: [],
      newMessage: '',
    };
  },
  created() {
    this.fetchModels();
  },
  methods: {
    async fetchModels() {
      try {
        const response = await fetch(`/api/models`);
        const data = await response.json();
        this.models = data;
        console.log('Models:', this.models);
        if (data.length > 0) {
          this.selectedModel = data[0].model_id;
        }
      } catch (error) {
        console.error('Error fetching models:', error);
      }
    },
    async sendMessage() {
      if (!this.newMessage.trim()) return;

      const userMessage = {
        role: 'user',
        content: this.newMessage,
      };
      this.messages.push(userMessage);

      try {
        const response = await fetch(`/api/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            model: this.selectedModel,
            messages: this.messages,
          }),
        });
        const data = await response.json();

        const aiMessage = {
          role: 'assistant',
          content: data.reply,
          model: this.selectedModel,
        };
        this.messages.push(aiMessage);
      } catch (error) {
        console.error('Error sending message:', error);
      }

      this.newMessage = '';
    },
  },
};
</script>