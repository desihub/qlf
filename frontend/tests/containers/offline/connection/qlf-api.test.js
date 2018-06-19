import QlfApi from '../../../../src/containers/offline/connection/qlf-api';

describe('QlfApi', () => {
  beforeEach(() => {
    fetch.mockReset();
  });

  it('calls getQA', () => {
    QlfApi.getQA(1);
    expect(fetch).toBeCalledWith(
      'http://localhost:8001/dashboard/api/processing_history/1/?format=json',
      {
        headers: {
          _headers: {
            accept: ['application/json'],
            'content-type': ['application/json'],
          },
        },
        method: 'GET',
      }
    );
  });

  it('calls getLastProcess', () => {
    QlfApi.getLastProcess();
    expect(fetch).toBeCalledWith(
      'http://localhost:8001/dashboard/api/last_process/?format=json',
      {
        headers: {
          _headers: {
            accept: ['application/json'],
            'content-type': ['application/json'],
          },
        },
        method: 'GET',
      }
    );
  });

  it('calls reprocessExposure', () => {
    QlfApi.reprocessExposure(3);
    expect(fetch).toBeCalledWith(
      'http://localhost:8001/dashboard/api/add_exposure/?format=json&exposure_id=3',
      {
        headers: {
          _headers: {
            accept: ['application/json'],
            'content-type': ['application/json'],
          },
        },
        method: 'GET',
      }
    );
  });

  it('calls getProcessingHistoryById', () => {
    QlfApi.getProcessingHistoryById(3);
    expect(fetch).toBeCalledWith(
      'http://localhost:8001/dashboard/api/processing_history/3/?format=json',
      {
        headers: {
          _headers: {
            accept: ['application/json'],
            'content-type': ['application/json'],
          },
        },
        method: 'GET',
      }
    );
  });

  it('calls getCurrentConfiguration', () => {
    QlfApi.getCurrentConfiguration();
    expect(fetch).toBeCalledWith(
      'http://localhost:8001/dashboard/api/current_configuration/?format=json',
      {
        headers: {
          _headers: {
            accept: ['application/json'],
            'content-type': ['application/json'],
          },
        },
        method: 'GET',
      }
    );
  });

  it('calls getDefaultConfiguration', () => {
    QlfApi.getDefaultConfiguration();
    expect(fetch).toBeCalledWith(
      'http://localhost:8001/dashboard/api/default_configuration/?format=json',
      {
        headers: {
          _headers: {
            accept: ['application/json'],
            'content-type': ['application/json'],
          },
        },
        method: 'GET',
      }
    );
  });

  it('calls getQlConfig', () => {
    QlfApi.getQlConfig('flat');
    expect(fetch).toBeCalledWith(
      'http://localhost:8001/dashboard/api/qlconfig/?format=json&type=flat',
      {
        headers: {
          _headers: {
            accept: ['application/json'],
            'content-type': ['application/json'],
          },
        },
        method: 'GET',
      }
    );
  });

  it('calls getExposuresDateRange', () => {
    QlfApi.getExposuresDateRange();
    expect(fetch).toBeCalledWith(
      'http://localhost:8001/dashboard/api/exposures_date_range/',
      {
        headers: {
          _headers: {
            accept: ['application/json'],
            'content-type': ['application/json'],
          },
        },
        method: 'GET',
      }
    );
  });

  it('calls getFlavors', () => {
    QlfApi.getFlavors();
    expect(fetch).toBeCalledWith(
      'http://localhost:8001/dashboard/api/distinct_flavors/',
      {
        headers: {
          _headers: {
            accept: ['application/json'],
            'content-type': ['application/json'],
          },
        },
        method: 'GET',
      }
    );
  });

  it('calls getProcessingHistory', () => {
    QlfApi.getProcessingHistory(
      '2019-01-01',
      '2019-01-01',
      '-pk',
      '2',
      '10',
      null
    );
    expect(fetch).toBeCalledWith(
      'http://localhost:8001/dashboard/api/processing_history/?format=json&limit=10&offset=2&ordering=-pk&datemin=2019-01-01&datemax=2019-01-01&null',
      {
        headers: {
          _headers: {
            accept: ['application/json'],
            'content-type': ['application/json'],
          },
        },
        method: 'GET',
      }
    );
  });

  it('calls getObservingHistory', () => {
    QlfApi.getObservingHistory(
      '2019-01-01',
      '2019-01-01',
      '-pk',
      '2',
      '10',
      null
    );
    expect(fetch).toBeCalledWith(
      'http://localhost:8001/dashboard/api/observing_history/?format=json&limit=10&offset=2&ordering=-pk&datemin=2019-01-01&&datemax=2019-01-01&null',
      {
        headers: {
          _headers: {
            accept: ['application/json'],
            'content-type': ['application/json'],
          },
        },
        method: 'GET',
      }
    );
  });

  it('calls addProcessComment', () => {
    QlfApi.addProcessComment('testing configuration', 1);
    expect(fetch).toBeCalledWith(
      'http://localhost:8001/dashboard/api/process_comment/',
      {
        body: '{"text":"testing configuration","process":1,"user":1}',
        headers: {
          _headers: {
            accept: ['application/json'],
            'content-type': ['application/json'],
          },
        },
        method: 'POST',
      }
    );
  });

  it('calls deleteProcessComment', () => {
    QlfApi.deleteProcessComment(3);
    expect(fetch).toBeCalledWith(
      'http://localhost:8001/dashboard/api/process_comment/3/',
      {
        headers: {
          _headers: {
            accept: ['application/json'],
            'content-type': ['application/json'],
          },
        },
        method: 'DELETE',
      }
    );
  });

  it('calls updateProcessComment', () => {
    QlfApi.updateProcessComment(3, 1, 'update comment');
    expect(fetch).toBeCalledWith(
      'http://localhost:8001/dashboard/api/process_comment/3/',
      {
        body: '{"text":"update comment","process":1}',
        headers: {
          _headers: {
            accept: ['application/json'],
            'content-type': ['application/json'],
          },
        },
        method: 'PUT',
      }
    );
  });

  it('calls getProcessComments', () => {
    QlfApi.getProcessComments(1);
    expect(fetch).toBeCalledWith(
      'http://localhost:8001/dashboard/api/process_comment/?process=1',
      {
        headers: {
          _headers: {
            accept: ['application/json'],
            'content-type': ['application/json'],
          },
        },
        method: 'GET',
      }
    );
  });

  it('calls sendTicketMail', () => {
    QlfApi.sendTicketMail('hawk@tes.com', 'test', 'problem', 'hawk');
    expect(fetch).toBeCalledWith(
      'http://localhost:8001/send_ticket_email/?format=json&email=hawk@tes.com&message=test&subject=problem&name=hawk',
      {
        headers: {
          _headers: {
            accept: ['application/json'],
            'content-type': ['application/json'],
          },
        },
        method: 'GET',
      }
    );
  });
});
