'use client';

import { DollarSign, TrendingUp, TrendingDown, Calculator, Euro } from 'lucide-react';
import React, { useMemo } from 'react';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { useTranslation } from '@/lib/i18n/use-translations';
import { usePropertyContext } from './property-context';

export function PropertyFinancialsTab() {
  const { t } = useTranslation();
  const { property, propertyId, formatCurrency } = usePropertyContext();

  // Mock data - replace with actual API calls when available
  const financialData = useMemo(() => ({
    monthlyRevenue: property?.monthlyRevenue || 45000,
    monthlyExpenses: property?.monthlyExpenses || 12000,
    yearlyRevenue: property?.yearlyRevenue || 540000,
    yearlyExpenses: property?.yearlyExpenses || 144000,
    occupancyRate: property?.occupancyRate || 0.95,
    totalUnits: property?.totalUnits || 24,
  }), [property]);

  const calculatedMetrics = useMemo(() => {
    const monthlyProfit = financialData.monthlyRevenue - financialData.monthlyExpenses;
    const yearlyProfit = financialData.yearlyRevenue - financialData.yearlyExpenses;
    const profitMargin = (monthlyProfit / financialData.monthlyRevenue) * 100;
    const revenuePerUnit = financialData.monthlyRevenue / financialData.totalUnits;
    
    return {
      monthlyProfit,
      yearlyProfit,
      profitMargin,
      revenuePerUnit,
    };
  }, [financialData]);



  const formatPercentage = (value: number) => {
    return `${value.toFixed(1)}%`;
  };

  return (
    <div className="space-y-6">
      {/* Financial Overview Cards */}
      <div className="grid gap-4 grid-cols-1 md:grid-cols-2 xl:grid-cols-4">
        {/* Monthly Revenue */}
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-secondary-500 dark:text-secondary-400">
                  Revenus mensuels
                </p>
                <h3 className="text-2xl font-bold text-secondary-900 dark:text-white">
                  {formatCurrency(financialData.monthlyRevenue)}
                </h3>
              </div>
              <div className="p-2 bg-success-100 dark:bg-success-900/20 rounded-full">
                <TrendingUp className="h-6 w-6 text-success-600 dark:text-success-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Monthly Expenses */}
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-secondary-500 dark:text-secondary-400">
                  Charges mensuelles
                </p>
                <h3 className="text-2xl font-bold text-secondary-900 dark:text-white">
                  {formatCurrency(financialData.monthlyExpenses)}
                </h3>
              </div>
              <div className="p-2 bg-error-100 dark:bg-error-900/20 rounded-full">
                <TrendingDown className="h-6 w-6 text-error-600 dark:text-error-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Monthly Profit */}
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-secondary-500 dark:text-secondary-400">
                  Bénéfice mensuel
                </p>
                <h3 className="text-2xl font-bold text-secondary-900 dark:text-white">
                  {formatCurrency(calculatedMetrics.monthlyProfit)}
                </h3>
                <p className="text-sm text-secondary-500 dark:text-secondary-400">
                  Marge: {formatPercentage(calculatedMetrics.profitMargin)}
                </p>
              </div>
              <div className="p-2 bg-primary-100 dark:bg-primary-900/20 rounded-full">
                <Calculator className="h-6 w-6 text-primary-600 dark:text-primary-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Revenue per Unit */}
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-secondary-500 dark:text-secondary-400">
                  Revenu par lot
                </p>
                <h3 className="text-2xl font-bold text-secondary-900 dark:text-white">
                  {formatCurrency(calculatedMetrics.revenuePerUnit)}
                </h3>
                <p className="text-sm text-secondary-500 dark:text-secondary-400">
                  {financialData.totalUnits} lots au total
                </p>
              </div>
              <div className="p-2 bg-warning-100 dark:bg-warning-900/20 rounded-full">
                <Euro className="h-6 w-6 text-warning-600 dark:text-warning-400" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Annual Summary */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <DollarSign className="h-5 w-5 text-primary-600" />
            Résumé financier annuel
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-6 md:grid-cols-2">
            <div className="space-y-4">
              <h4 className="font-semibold text-secondary-900 dark:text-white">Revenus</h4>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-secondary-600 dark:text-secondary-400">Revenus annuels</span>
                  <span className="font-medium">{formatCurrency(financialData.yearlyRevenue)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-secondary-600 dark:text-secondary-400">Taux d'occupation</span>
                  <span className="font-medium">{formatPercentage(financialData.occupancyRate * 100)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-secondary-600 dark:text-secondary-400">Revenu potentiel max</span>
                  <span className="font-medium">
                    {formatCurrency(financialData.yearlyRevenue / financialData.occupancyRate)}
                  </span>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <h4 className="font-semibold text-secondary-900 dark:text-white">Charges et bénéfices</h4>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-secondary-600 dark:text-secondary-400">Charges annuelles</span>
                  <span className="font-medium text-error-600">
                    -{formatCurrency(financialData.yearlyExpenses)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-secondary-600 dark:text-secondary-400">Bénéfice annuel</span>
                  <span className="font-bold text-success-600">
                    {formatCurrency(calculatedMetrics.yearlyProfit)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-secondary-600 dark:text-secondary-400">Rendement</span>
                  <span className="font-medium">
                    {formatPercentage((calculatedMetrics.yearlyProfit / financialData.yearlyRevenue) * 100)}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Financial Categories Breakdown */}
      <Card>
        <CardHeader>
          <CardTitle>Répartition des charges mensuelles</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {/* Mock expense categories - replace with real data */}
            {[
              { name: 'Charges de copropriété', amount: 4800, color: 'bg-blue-500' },
              { name: 'Assurances', amount: 1200, color: 'bg-green-500' },
              { name: 'Maintenance et réparations', amount: 2400, color: 'bg-yellow-500' },
              { name: 'Taxes foncières', amount: 2000, color: 'bg-red-500' },
              { name: 'Gestion et administration', amount: 1600, color: 'bg-purple-500' },
            ].map((category, index) => {
              const percentage = (category.amount / financialData.monthlyExpenses) * 100;
              return (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className={`w-3 h-3 rounded-full ${category.color}`} />
                    <span className="text-secondary-700 dark:text-secondary-300">{category.name}</span>
                  </div>
                  <div className="text-right">
                    <div className="font-medium">{formatCurrency(category.amount)}</div>
                    <div className="text-sm text-secondary-500">{formatPercentage(percentage)}</div>
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Future enhancements placeholder */}
      <Card>
        <CardHeader>
          <CardTitle>Évolution financière</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-secondary-500 dark:text-secondary-400">
            <Calculator className="w-16 h-16 mx-auto mb-4 opacity-50" />
            <p>Graphiques d'évolution des revenus et charges</p>
            <p className="text-sm">À implémenter avec les données historiques</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
} 