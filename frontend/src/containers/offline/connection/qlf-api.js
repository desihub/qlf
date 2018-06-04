const apiUrl = process.env.REACT_APP_API;
const headers = new Headers({
  Accept: 'application/json',
  'Content-Type': 'application/json',
});

export default class QlfApi {
  static async getQA(processId) {
    try {
      const qa = await fetch(
        `${apiUrl}dashboard/api/processing_history/${processId}/?format=json`,
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

  static async getCurrentConfiguration() {
    try {
      const configuration = await fetch(
        `${apiUrl}dashboard/api/default_configuration/?format=json`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await configuration.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async getDefaultConfiguration() {
    try {
      const configuration = await fetch(
        `${apiUrl}dashboard/api/default_configuration/?format=json`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await configuration.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async getQlConfig() {
    try {
      const configuration = await fetch(
        `${apiUrl}dashboard/api/qlconfig/?format=json`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await configuration.json();
      return responseJson;
    } catch (e) {
      return null;
    }
  }

  static async getQlCalibration() {
    try {
      const configuration = await fetch(
        `${apiUrl}dashboard/api/ql_calibration/?format=json`,
        {
          method: 'GET',
          headers: headers,
        }
      );
      const responseJson = await configuration.json();
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

  static async getFlavors() {
    try {
      const exposures = await fetch(
        `${apiUrl}dashboard/api/distinct_flavors/`,
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

  static async getProcessingHistory(start, end, order, offset, limit, filters) {
    if (!start && !end) return;
    try {
      const processes = await fetch(
        `${apiUrl}dashboard/api/processing_history/?format=json&limit=${
          limit
        }&offset=${offset}&ordering=${order}&datemin=${
          start.split('T')[0]
        }&datemax=${end.split('T')[0]}&${filters}`,
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

  static async getObservingHistory(start, end, order, offset, limit, filters) {
    if (!start && !end) return;
    try {
      const exposures = await fetch(
        `${apiUrl}dashboard/api/observing_history/?format=json&limit=${
          limit
        }&offset=${offset}&ordering=${order}&datemin=${
          start.split('T')[0]
        }&&datemax=${end.split('T')[0]}&${filters}`,
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
