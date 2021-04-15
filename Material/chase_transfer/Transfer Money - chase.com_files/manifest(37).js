define({version:2,area:{module:"securityCenter/area",viewPath:{prefix:"securityCenter/views/"},dependencies:{"./css/securityCenter.css":"css"},services:{securityCenterOverviewService:{module:"securityCenter/services/securityCenterOverview"},aggregatorContent:{module:"common/lib/thirdPartyAccess/service/aggregatorContent"},externalAccountsService:{module:"securityCenter/services/externalAccounts"},reportFraudService:{module:"securityCenter/services/reportFraud"}},controllers:{overview:{module:"securityCenter/controllers/securityCenter/overview",components:{overview:{module:"securityCenter/components/securityCenter/overview",spec:"bluespec/account_safe_menu"}},immediate:!0},detail:{module:"securityCenter/controllers/securityCenter/detail",components:{detail:{module:"securityCenter/components/securityCenter/detail",spec:"bluespec/account_safe_menu",model:"accountSafeDetail",modelCleanup:!0},breadcrumb:{module:"securityCenter/components/securityCenter/breadcrumb",spec:"bluespec/account_safe_breadcrumb",model:"accountSafeBreadcrumb",modelCleanup:!0}}},dataPrivacy:{immediate:!0,module:"securityCenter/controllers/dataPrivacy/dataPrivacy",components:{dataPrivacy:{module:"securityCenter/components/dataPrivacy/dataPrivacy",spec:"bluespec/data_privacy"}}},reportFraud:{immediate:!0,module:"securityCenter/controllers/reportFraud/reportFraud",components:{reportFraud:{module:"securityCenter/components/reportFraud/reportFraud",spec:"bluespec/report_fraud"}}},savedAccountManager:{block:"savedAccountManager",immediate:!1}}}});