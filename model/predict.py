import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics
import numpy as np
def data_handle(method='W', fill=0):
    """
    :param method: 数据处理粒度：W代表周，D代表天
    :return:
    """
    # 进行数据的日期填充
    data = pd.read_excel('TS46131170.xlsx')
    data = data[data['销售数量'] > 0]
    data_new = pd.concat([data, data['销售日期'].dt.isocalendar()], axis=1)
    date = pd.date_range(min(data['销售日期']), max(data['销售日期']), freq=method).isocalendar()
    # print(max(data['销售日期']))

    if method == 'W':
        sale = pd.merge(data_new.groupby(['year', 'week']).sum()['销售数量'], date.groupby(['year', 'week']).sum(),
                        left_index=True, right_index=True, how='right').fillna(fill)
        data_new = sale['销售数量']
        data_new.index = pd.date_range(min(data['销售日期']), max(data['销售日期']), freq=method)

    elif method == 'D':
        sale = pd.merge(data_new.groupby(['year', 'week', 'day']).sum()['销售数量'], date.groupby(['year', 'week', 'day']).sum(),
                        left_index=True, right_index=True, how='right').fillna(fill)
        data_new = sale['销售数量']
    return data_new
    
# print(data_handle(method='W'))

class Predict:
    def __init__(self):
        self.data = data_handle(method='W')

    def generate(self, windows):
        from sklearn.model_selection import train_test_split
        X = []
        Y = []
        Y_label = []
        for i in range(len(self.data)-windows):
            X.append(self.data.values[i:i+windows])
            Y.append([self.data.values[i+windows],str([self.data.index[[i+windows]].year.values[0], self.data.index[[i+windows]].month.values[0]])])
            Y_label.append(str([self.data.index[[i+windows]].year.values[0], self.data.index[[i+windows]].month.values[0]]))
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=20)
        return X_train, X_test, [i[0] for i in y_train], [i[0] for i in y_test], [i[1] for i in y_train], [i[1] for i in y_test]

    def pre(self, method, X_train, X_test, y_train, y_test, y_test_index):

        from sklearn import svm
        from sklearn import linear_model
        from sklearn.neighbors import KNeighborsRegressor

        if method == 'SVR':
            reg = svm.SVR()
            reg.fit(X_train, y_train)
            nn = reg.predict(X_test)
        elif method == 'Linear':
            reg = linear_model.LinearRegression()
            reg.fit(X_train, y_train)
            nn = reg.predict(X_test)
        elif method == 'KNeighbors':
            reg = KNeighborsRegressor(n_neighbors=3)
            reg.fit(X_train, y_train)
            nn = reg.predict(X_test)
        elif method == 'RF':
            from sklearn import tree
            reg = tree.DecisionTreeRegressor()
            reg.fit(X_train, y_train)
            nn = reg.predict(X_test)
        elif method == 'MLP':
            from sklearn.neural_network import MLPRegressor
            reg = MLPRegressor(random_state=4, max_iter=500)
            reg.fit(X_train, y_train)
            nn = reg.predict(X_test)
        elif method == 'AVERAGE':
            nn = [np.mean(i) for i in X_test]
        plt.plot(nn, color='blue')
        plt.plot(y_test, color='red')
        plt.title(method)
        plt.show()
        from sklearn import metrics
        print('######################' + method + '###################################')
        print(metrics.r2_score(y_test, nn))
        res = pd.DataFrame(data=np.array([y_test_index, y_test, list(nn)]).transpose(), columns=['time', 'true', 'predict'])
        res['true'] = res['true'].apply(float)
        res['predict'] = res['predict'].apply(float)
        print(res.groupby('time').sum())
        print('######################end##############################################')


if __name__ == '__main__':
    X_train, X_test, y_train, y_test, y_train_index, y_test_index = Predict().generate(4)
    method = ['SVR', 'Linear', 'KNeighbors', 'RF', 'MLP', 'AVERAGE']
    for m_ in method:
        Predict().pre(m_, X_train, X_test, y_train, y_test, y_test_index )





