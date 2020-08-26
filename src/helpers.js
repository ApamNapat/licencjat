import {notification} from "antd";

export const notifyOfAPIFailure = (error) => {
    notification.open({
        message: 'Something went wrong getting/posting data',
        description: `Error message: ${error.message}`,
        placement: 'bottomLeft',
    });
};

export const urlBase = 'http://localhost:8000/';
