const { createApp } = Vue;

createApp({
    data() {
        return {
            count: 0,
            message: '',
            messages: [],
            loading: false,
            intro: [
                { title: 'Examples', lines: [] }
            ]
        };
    },
    methods: {
        select(id) {
            if(id == 1)
                this.message = 'Who can approve the OEM OES Nomination case ?'
            else 
                this.message = 'What are the conditions for vendor banning ?'
            this.send();
        },
        async send() {
            this.messages.push({ id: ++this.count, content: this.message, author: 'human' });
            this.loading = true
            
            var response = await axios.post('/query', { query: this.message })
            
            this.loading = false
            this.message = '';
            this.messages.push({ id: ++this.count, content: response.data.answer, author: 'ai' });
        },
    },
}).mount("#app");
