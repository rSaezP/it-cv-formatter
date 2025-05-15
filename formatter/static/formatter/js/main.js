// Aplicación Vue principal
const app = new Vue({
    el: '#app',
    data: {
        isProcessing: false,
        fileName: '',
        templateName: '',
        showPreview: false
    },
    methods: {
        onSubmit: function(e) {
            this.isProcessing = true;
            // El formulario se enviará normalmente
        },
        updateFileName: function(event) {
            const fileInput = event.target;
            if (fileInput.files.length > 0) {
                this.fileName = fileInput.files[0].name;
            } else {
                this.fileName = '';
            }
        },
        updateTemplateName: function(event) {
            const fileInput = event.target;
            if (fileInput.files.length > 0) {
                this.templateName = fileInput.files[0].name;
            } else {
                this.templateName = '';
            }
        }
    }
});
