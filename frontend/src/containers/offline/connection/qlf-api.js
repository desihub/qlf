const apiUrl = process.env.REACT_APP_API;
const headers = new Headers({
  Accept: 'application/json',
  'Content-Type': 'application/json',
});

export default class QlfApi {
  static async getQA(processId) {
    try {
      const qa = await fetch(
        `${apiUrl}dashboard/api/single_qa/${processId}/?format=json`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await qa.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async getLastProcess() {
    try {
      const processes = await fetch(
        `${apiUrl}dashboard/api/last_process/?format=json`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await processes.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async reprocessExposure(exposure) {
    try {
      const processes = await fetch(
        `${apiUrl}dashboard/api/add_exposure/?format=json&exposure_id=${
          exposure
        }`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await processes.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async getProcessingHistory() {
    try {
      const processes = await fetch(
        `${apiUrl}dashboard/api/processing_history/?format=json`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await processes.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async getProcessingHistoryById(processId) {
    try {
      const processes = await fetch(
        `${apiUrl}dashboard/api/processing_history/${processId}/?format=json`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await processes.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async getProcessingHistoryLimit() {
    try {
      const processes = await fetch(
        `${apiUrl}dashboard/api/processing_history/?format=json&limit=10`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await processes.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async getProcessingHistoryOrdered(order) {
    try {
      const processes = await fetch(
        `${apiUrl}dashboard/api/processing_history/?format=json&ordering=${
          order
        }`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await processes.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async getProcessingHistoryRangeDate(start, end) {
    try {
      const processes = await fetch(
        `${apiUrl}dashboard/api/processing_history/?format=json&datemin=${
          start
        }&&datemax=${end}`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await processes.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async getObservingHistory() {
    try {
      const exposures = await fetch(
        `${apiUrl}dashboard/api/observing_history/?format=json`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await exposures.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async getExposuresDateRange() {
    try {
      const exposures = await fetch(
        `${apiUrl}dashboard/api/exposures_date_range/`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await exposures.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async getObservingHistoryOrdered(order) {
    try {
      const exposures = await fetch(
        `${apiUrl}dashboard/api/observing_history/?format=json&ordering=${
          order
        }`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await exposures.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async getObservingHistoryRangeDate(start, end) {
    try {
      const exposures = await fetch(
        `${apiUrl}dashboard/api/observing_history/?format=json&datemin=${
          start
        }&&datemax=${end}`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await exposures.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async sendTicketMail(email, message, subject, name) {
    const ticket = await fetch(
      `${apiUrl}send_ticket_email/?format=json&email=${email}&message=${
        message
      }&subject=${subject}&name=${name}`,
      {
        method: 'GET',
        headers: headers,
      }
    );
    const responseJson = await ticket.json();
    return responseJson;
  }
}
