const assert=require('node:assert/strict');
var UI={de:{reviewed:'YES'},es:{reviewed:'YES'},en:{reviewed:'YES'}};var lang='de';
  function approvalLine(q) {
    var r = q.review || {}, a = r.approval || {};
    return r.approval_valid === true && (a.languages || []).indexOf(lang) >= 0
      ? UI[lang].reviewed + ': ' + r.last_reviewed + ' · ' + r.reviewer + ' · ' + a.languages.join(', ').toUpperCase()
      : '';
  }
let q={review:{reviewer:'TEST ONLY',last_reviewed:'2026-09-12',approval_valid:true,approval:{languages:['de']}}};assert.match(approvalLine(q),/^YES/);lang='es';assert.equal(approvalLine(q),'');lang='en';assert.equal(approvalLine(q),'');lang='de';q.review.approval_valid=false;assert.equal(approvalLine(q),'');q.review.approval_valid=true;q.review.expires='2000-01-01';q.review.approval.expires='2000-01-01';assert.match(approvalLine(q),/^YES/);console.log('5 approval display checks passed');