import {notification} from "antd";

export const notifyOfAPIFailure = (error: Error) => {
    notification.open({
        message: 'Something went wrong getting/posting data',
        description: `Error message: ${error.message}`,
        placement: 'bottomLeft',
    });
};

export const urlBase = 'https://iidle.herokuapp.com/';
