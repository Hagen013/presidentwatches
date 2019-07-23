import request from '@/utils/request'
const equal = require('fast-deep-equal');


export default {
    data: () => ({
        initialized: false,
        listApiUrl: '',
        instanceId: null,
        instance: {
        },
        instanceProxy: {
        },
        responseReceived: false,
        requestError: false,
        hasChanged: false,
        showDeleteDialog: false,
        notificationTitle: 'Успешно',
        notificationMessage: 'Запись успешно сохранена'
    }),
    computed: {
        instanceApiUrl() {
            if (this.instanceId !== null) {
                return `${this.listApiUrl}${this.instanceId}/`
            }
            return null
        },
        loading() {

        }
    },
    created() {
        this.initialize();
    },
    methods: {
        initialize() {
            let instanceId = this.$route.params.id;
            if (instanceId !== undefined) {
                this.instanceId = instanceId;
                this.getInstance();
            } else {
                this.responseReceived = true;
            }
            this.initialized = true;
        },

        // Changes handling methods START
        //-------------------------------
        checkChanges() {
            this.hasChanged = !equal(this.instance, this.instanceProxy);
        },
        saveChanges() {
            this.updateInstance();
        },
        rollbackChanges() {
            this.instanceProxy = JSON.parse(JSON.stringify(this.instance));
            this.checkChanges();
        },
        // Changes handling methods END
        //-------------------------------

        triggerDelete() {
            this.showDeleteDialog = true;
        },
        cofirmDelete() {
            this.showDeleteDialog = false;
            this.deleteInstance();
        },
        cancelDelete() {
            this.showDeleteDialog = false;
        },

        //-------------------------------
        // CRUD methods START
        createInstance() {
            this.responseReceived = false;
            this.requestError = false;
            request.post(this.instanceApiUrl, this.instance).then(
                response => {
                    this.handleSuccessfulCreateResponse(response);
                },
                response => {
                    this.handleFailedCreateResponse(response);
                }
            )
        },
        getInstance() {
            this.responseReceived = false;
            this.requestError = false;
            request.get(this.instanceApiUrl).then(
                response => {
                    this.handleSuccessfulGetInstanceResponse(response);
                },
                response => {
                    this.handleFailedGetInstanceResponse(response);
                }
            )
        },
        updateInstance() {
            this.responseReceived = false;
            this.requestError = false;
            request.put(this.instanceApiUrl, this.instance).then(
                response => {
                    this.handleSuccessfulUpdateResponse(response);
                },
                response => {
                    this.handleFailedUpdateResponse(response);
                }
            )
        },
        deleteInstance() {
            this.responseReceived = false;
            this.requestError = false;
            request.delete(this.instanceApiUrl).then(
                response => {
                    this.handleSuccessfulDeleteResponse(response);
                },
                response => {
                    this.handleFailedDeleteResponse(response);
                }
            )
        },
        // CRUD methods END
        //-------------------------------

        //-------------------------------
        // CRUD handlers START
        // CREATE handlers
        handleSuccessfulCreateResponse(response) {
        },
        handleFailedCreateResponse(response) {
        },
        // READ handlers
        handleSuccessfulGetInstanceResponse(response) {
            this.instance = response.data;
            this.instanceProxy = JSON.parse(JSON.stringify(this.instance));
            this.responseReceived = true;
            this.requestError = false;
            this.postInitialize();
        },
        handleFailedGetInstanceResponse(response) {
            this.responseReceived = true;
            this.requestError = true;
        },
        postInitialize() {

        },
        // UPDATE handlers
        handleSuccessfulUpdateResponse(response) {
            this.instance = response.data;
            this.instanceProxy = JSON.parse(JSON.stringify(this.instance));
            this.responseReceived = true;
            this.requestError = false;
            this.$notify({
                title: this.notificationTitle,
                message: this.notificationMessage,
                type: 'success'
              });
        },
        handleFailedUpdateResponse(response) {
            this.responseReceived = true;
            this.requestError = true;
        },
        // DELETE handlers
        handleSuccessfulDeleteResponse(response) {
        },
        handleFailedDeleteResponse(response) {
        }
        // CRUD handlers END
        //-------------------------------
    
    },
    watch: {
        instance: {
            handler() {
                this.checkChanges();
            },
            deep: true
        }
    }
}
